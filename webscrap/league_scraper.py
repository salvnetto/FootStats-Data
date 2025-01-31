from typing import List, Tuple
import time
import pandas as pd

from http_client import HTTPClient, ScraperConfig
from webscrap.parser import DataParser
from data_saver import DataSaver
from exceptions import ScraperError
from constants import URL_FBREF




class LeagueScraper:
    def __init__(
        self,
        missing_seasons: List[str],
        league_config: object,
        base_path: str = "datasets",
        config: ScraperConfig = ScraperConfig()
    ):
        self.missing_seasons = missing_seasons
        self.league_config = league_config
        self.config = config
        
        self.http_client = HTTPClient(retries=config.max_retries)
        self.parser = DataParser()
        self.data_saver = DataSaver(base_path, league_config.league_code)

    def scrape(self) -> None:
        """Main scraping process."""
        for season in self.missing_seasons:
            print(f"Season: {season}")
            try:
                self._scrape_season(season)
            except ScraperError as e:
                print(f"Error scraping season {season}: {e}")
                continue

    def _scrape_season(self, season: str) -> None:
        """Scrape data for a specific season."""
        # Get league URL
        league_url = self._build_league_url(season)
        
        # Get team URLs
        response = self.http_client.get(league_url)
        team_urls = self.parser.parse_team_urls(response.text)
        
        # Process each team
        squad_data = []
        match_history_data = []

        for team_url in team_urls:
            try:
                squad_df, mh_df = self._process_team(team_url, season)
                squad_data.append(squad_df)
                match_history_data.append(mh_df)
                time.sleep(self.config.request_delay)
            except ScraperError as e:
                print(f"Error processing team {team_url}: {e}")
                continue
        
        # Combine and save data
        combined_squad = pd.concat(squad_data, ignore_index=True)
        combined_mh = pd.concat(match_history_data, ignore_index=True)
        self.data_saver.save_season_data(combined_squad, combined_mh, season)

    def _build_league_url(self, season: str) -> str:
        """Build the league URL for a given season."""
        return f"{URL_FBREF}/en/comps/{self.league_config.id}/{season}/{season}-{self.league_config.name_code}-Stats"

    def _process_team(self, team_url: str, season: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Process data for a single team."""
        team_name = team_url.split('/')[-1].replace('-Stats', '').replace('-', '_').lower()
        response = self.http_client.get(team_url)
        print(f"-{team_name}")
        return self.parser.parse_team_data(response.text, team_name, self.league_config.name, season)
