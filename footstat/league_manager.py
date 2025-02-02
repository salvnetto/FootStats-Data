from typing import Optional

from footstat.config import ConfigManager, LeagueConfig
from footstat.validators import LeagueValidator
from footstat.season_manager import SeasonManager
from footstat.league_scraper import LeagueScraper
from footstat.processer import DataProcessor


class LeagueDataManager:
    def __init__(
        self,
        country: str,
        league_code: str,
        config_path: Optional[str] = None
    ) -> None:
        """
        Initialize the league data manager.
        
        Args:
            country: Country code
            league_code: League code
            config_path: Optional path to config file
        """
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        
        # Validate inputs
        LeagueValidator.validate_league_config(self.config, country, league_code)
        
        # Set up league configuration
        self.league_config = LeagueConfig(
            country=country,
            league_code=league_code,
            name = self.config[country][league_code]['name'],
            name_code = self.config[country][league_code]['name_code'],
            id = self.config[country][league_code]['id'],
            calendar=self.config[country][league_code]['calendar']
        )

        # Initialize season manager
        self.season_manager = SeasonManager(
            self.config_manager.project_root,
            league_code,
            self.league_config.calendar
        )
        
        # Get missing seasons
        self.missing_seasons = self.season_manager.get_missing_seasons()
        print(self.missing_seasons)
    
        # Scrape
        self.scraper = LeagueScraper(
            self.missing_seasons,
            self.league_config
           )
        self.scraper.scrape()

        # Processer
        self.processer = DataProcessor(
            league_config=self.league_config,
            base_path="datasets"
            )