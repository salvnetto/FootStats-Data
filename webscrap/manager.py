import json
import re
import os
from pathlib import Path

from seasons import AVAILABLE_SEASONS


class LeagueDataManager:
    def __init__(self, country, league_code, leagues_db: str | None = None) -> None:
        """
        Initializes the scraper with a dynamic default path to leagues.json.
        
        Args:
            leagues_db (str | None): Custom path to the JSON file. If None, uses:
                project_root/database/leagues.json
        """

        if leagues_db is None:
            # Get path relative to this file's location
            script_dir = Path(__file__).parent  # webscrap directory
            self.project_root = script_dir.parent    # Go up to project root
            leagues_db = f"{self.project_root}/database/leagues.json"
            
        self._load_db(leagues_db)
        self._validate_country_and_league_code(country, league_code)
        
        # Sets up the actual league
        self.league = self.league.get(self.country).get(self.league_code)
        self._detect_missing_seasons()

    def _load_db(self, db_file: str) -> None:
        """
        Loads the database from the provided JSON file.
        
        Args:
            db_file (str): Path to the JSON file containing leagues database.
        
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        try:
            if not Path(db_file).exists():
                raise FileNotFoundError(f"Database file not found: {db_file}")
            
            with open(db_file, 'r') as file:
                self.league = json.load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.league = {}
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {db_file}: {e}")
            self.league = {}
        except Exception as e:
            print(f"Unexpected error loading database: {e}")
            self.league = {}

    def _validate_country_and_league_code(self, country, league_code):
        try:
            # Check if the country exists
            if country not in self.league:
                raise ValueError(f"Invalid country '{country}'.")
            # Check if the league_code exists for the given country
            if league_code not in self.league[country]:
                raise ValueError(f"Invalid league code '{league_code}' for country '{country}'.")
            self.country = country
            self.league_code = league_code

        except ValueError as e:
            print(e)
            if 'Invalid country' in str(e):
                print("\nAvailable countries:")
                for index, country in enumerate(self.league.keys(), 1):
                    print(f"{index}. {country}")
            if 'Invalid league code' in str(e):
                print(f"\nAvailable league codes for '{country}':")
                for index, league_code in enumerate(self.league[country].keys(), 1):
                    print(f"{index}. {league_code}")

    def _detect_missing_seasons(self):
        """
        """
        try:
            # Define the datasets path
            datasets_path = f"{self.project_root}/datasets/raw_data/{self.league_code}"

            # Check if the directory exists, if not create it
            if not os.path.exists(datasets_path):
                os.makedirs(datasets_path)

            # List files in the directory
            files = [f.name for f in Path(datasets_path).iterdir() if f.is_file()]

            # Split files into match history and squads
            match_history = [file for file in files if 'match_history' in file]
            squads = [file for file in files if 'squads' in file]

            # Regular expression pattern for season extraction
            seasons_pattern = re.compile(r'(\d{4}-\d{4}|\d{4})')

            self.missing_seasons = []
            for files_ in (match_history, squads):
                extracted_seasons = [seasons_pattern.search(filename).group(0) for filename in files_]
                missing_from_extracted_seasons = [season for season in AVAILABLE_SEASONS[self.league['calendar']-1] if season not in extracted_seasons]
                self.missing_seasons.append(missing_from_extracted_seasons)

        except Exception as e:
            print(f"Error: {e}")

    def scrape(self):
        self.missing_seasons
        self.league
        #Will call a another scraper class
