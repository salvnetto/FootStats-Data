from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List
import hashlib
import unicodedata
import base64
import pandas as pd
import re

from footstat.constants import NAME_CHANGES



class FileType(Enum):
    MATCH_HISTORY = "match_history"
    SQUADS = "squad"

@dataclass
class ProcessingConfig:
    columns_to_drop: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.columns_to_drop is None:
            self.columns_to_drop = {
                'match_history': ['match report'],
                'squads': ['matches_90']
            }

class DataTransformer:
    """Handles data transformation operations."""
    
    @staticmethod
    def create_hash_key(input_string: str) -> str:
        """Create a unique hash key from input string."""
        # Normalize and clean input
        input_string = input_string.lower()
        normalized = unicodedata.normalize('NFD', input_string)
        cleaned = ''.join(
            char for char in normalized 
            if unicodedata.category(char) != 'Mn'
        )
        
        # Generate hash
        hash_object = hashlib.sha256()
        hash_object.update(cleaned.encode('utf-8'))
        hash_bytes = hash_object.digest()
        hash_base64 = base64.urlsafe_b64encode(hash_bytes).decode('utf-8').rstrip('=')
        
        return f"{hash_base64[:9]}{cleaned[:3]}"

    @staticmethod
    def remove_numbers_from_string(text: str) -> str:
        """Remove leading numbers from string."""
        return re.sub(r'^\d{4}\s+', '', text)

    @staticmethod
    def change_opponent(team_name: str) -> str:
        """Map team names to their standardized versions."""
        return NAME_CHANGES.get(team_name, team_name)

class DataFileManager:
    """Handles file operations for data processing."""
    
    def __init__(self, base_path: Path, league_code: str):
        self.raw_data_path = base_path / "raw_data" / league_code
        self.processed_data_path = base_path / "processed_data" / league_code
        self.processed_data_path.mkdir(parents=True, exist_ok=True)

    def combine_csv_files(self, file_prefix: str) -> pd.DataFrame:
        """Combine all CSV files with given prefix."""
        csv_files = list(self.raw_data_path.glob(f"{file_prefix}*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found with prefix: {file_prefix}")
            
        dataframes = [pd.read_csv(file) for file in csv_files]
        return pd.concat(dataframes, ignore_index=True)

    def save_processed_data(self, df: pd.DataFrame, file_name: str) -> None:
        """Save processed dataframe to CSV."""
        output_path = self.processed_data_path / f"{file_name}.csv"
        df.to_csv(output_path, index=False)

class DataProcessor:
    """Main class for processing sports data."""
    
    def __init__(
        self,
        league_config: object,
        base_path: str,
        config: ProcessingConfig = ProcessingConfig()
    ):
        self.league_config = league_config
        self.config = config
        self.file_manager = DataFileManager(Path(base_path), league_config.league_code)
        self.transformer = DataTransformer()
        # process
        self.process_file_type(FileType.MATCH_HISTORY)
        self.process_file_type(FileType.SQUADS)
        
    def process_file_type(self, file_type: FileType) -> None:
        """Process specific file type."""
        # Load and combine data
        df = self.file_manager.combine_csv_files(file_type.value)
        
        # Process based on file type
        processors = {
            FileType.SQUADS: self._process_squads,
            FileType.MATCH_HISTORY: self._process_match_history
        }
        
        processor = processors.get(file_type)
        if not processor:
            raise ValueError(f"Unsupported file type: {file_type}")
            
        # Process and save
        processed_df = processor(df)
        self.file_manager.save_processed_data(processed_df, file_type.value)

    def _process_common(self, df: pd.DataFrame, file_type: FileType) -> pd.DataFrame:
        """Common processing steps for all file types."""
        df = df.copy()
        # Convert columns to lowercase
        df.columns = df.columns.str.lower()
        
        # Drop specified columns
        columns_to_drop = self.config.columns_to_drop.get(file_type.value, [])
        df = df.drop(columns=columns_to_drop, errors='ignore')
        
        return df

    def _process_squads(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process squads data."""
        df = self._process_common(df, FileType.SQUADS)
        
        # Remove totals/averages
        df = df[~df['player'].isin(['Squad Total', 'Opponent Total'])]
        
        # Process team names and create IDs
        df['team_name'] = df['team_name'].apply(self.transformer.remove_numbers_from_string)
        df['team_id'] = df['team_name'].apply(self.transformer.create_hash_key)
        df = df.drop('matches_90', axis=1)
        
        return df

    def _process_match_history(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process match history data."""
        df = self._process_common(df, FileType.MATCH_HISTORY)
        
        # Filter for specific competition
        df = df[df['comp'] == self.league_config.name]
        
        # Process round numbers
        df['round'] = df['round'].str.replace("Matchweek ", "", regex=False)
        df['round'] = df['round'].astype(int)
        
        # Process team names and create IDs
        df['opponent'] = df['opponent'].apply(self.transformer.change_opponent)
        df['team_name'] = df['team_name'].apply(self.transformer.remove_numbers_from_string)
        df['team_opp_id'] = df['opponent'].apply(self.transformer.create_hash_key)
        df['team_id'] = df['team_name'].apply(self.transformer.create_hash_key)
        
        return df