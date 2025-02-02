import re
from datetime import datetime
from pathlib import Path
from typing import List

from footstat.exceptions import LeagueManagerError

CURRENT_DATE = datetime.now()
EARLIEST_SEASON = 2019

AVAILABLE_SEASONS = [
    [str(year) for year in range(EARLIEST_SEASON, CURRENT_DATE.year+1)],
    (
        [f"{year}-{year+1}" for year in range(2019, CURRENT_DATE.year) if CURRENT_DATE.month < 7] +
        [f"{year}-{year+1}" for year in range(2019, CURRENT_DATE.year + 1) if CURRENT_DATE.month >= 7]
    )
]

CURRENT_SEASON = [
    AVAILABLE_SEASONS[0][-1],
    AVAILABLE_SEASONS[1][-1]
]


class SeasonManager:
    def __init__(self, project_root: Path, league_code: str, calendar_type: int):
        self.datasets_path = project_root / "datasets" / "raw_data" / league_code
        self.calendar_type = calendar_type
        self.seasons_pattern = re.compile(r'(\d{4}-\d{4}|\d{4})')
        
    def ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        
    def get_missing_seasons(self) -> List[str]:
        """Returns a list of missing seasons."""
        try:
            self.ensure_data_directory()
            files = list(self.datasets_path.iterdir())
            
            match_files = [f.name for f in files if 'match_history' in f.name]
            squad_files = [f.name for f in files if 'squad' in f.name]
            
            match_seasons = self._get_missing_for_type(match_files)
            squad_seasons = self._get_missing_for_type(squad_files)
            
            missing_seasons = list(set(match_seasons + squad_seasons) - {CURRENT_SEASON[self.calendar_type-1]})
            return missing_seasons + [CURRENT_SEASON[self.calendar_type-1]]
        except Exception as e:
            raise LeagueManagerError(f"Error processing seasons: {e}")
    
    def _get_missing_for_type(self, files: List[str]) -> List[str]:
        extracted = [
            self.seasons_pattern.search(filename).group(0)
            for filename in files
        ]

        return [
            season for season in AVAILABLE_SEASONS[self.calendar_type - 1]
            if season not in extracted
        ]
