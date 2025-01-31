from typing import List, Tuple, Dict, Optional
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
from dataclasses import dataclass

from exceptions import ParsingError
from constants import STATISTICS, URL_FBREF
from http_client import HTTPClient
from league_scraper import ScraperConfig



class DataParser:
    """Main parser class for handling team and match data."""
    
    def __init__(self):
        self.statistics_parser = StatisticsParser()

    def parse_team_urls(self, html_content: str) -> List[str]:
        """Extract team URLs from league page."""
        try:
            soup = BeautifulSoup(html_content, features='lxml')
            table = soup.select('table.stats_table')[0]
            links = table.find_all('a')
            team_links = [
                f"https://fbref.com{link.get('href')}"
                for link in links
                if link.get('href') and '/squads/' in link.get('href')
            ]
            return team_links
        except Exception as e:
            raise ParsingError(f"Failed to parse team URLs: {str(e)}")

    def parse_team_data(
        self, 
        html_content: str, 
        team_name: str, 
        league_name: str, 
        season: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Parse squad and match history data from team page."""
        try:
            soup = BeautifulSoup(html_content, features='lxml')
            tables = pd.read_html(StringIO(html_content))
            
            # Process squad data
            squad_df = self._process_squad_data(tables[0], team_name, season)
            
            # Process match history
            match_history_df = self._process_match_history(
                tables[1], 
                team_name, 
                season, 
                league_name,
                soup
            )
            
            return squad_df, match_history_df
            
        except Exception as e:
            raise ParsingError(f"Failed to parse team data: {str(e)}")
    
    def _process_squad_data(
        self, 
        df: pd.DataFrame, 
        team_name: str, 
        season: str
    ) -> pd.DataFrame:
        """Process squad data with team and season information."""
        df = df.copy()
        df.columns = df.columns.droplevel()
        df.columns = [col if i <= 24 else f"{col}_90" for i, col in enumerate(df.columns)]
        df['team_name'] = team_name
        df['season'] = season
        return df
    
    def _process_match_history(
        self,
        df: pd.DataFrame,
        team_name: str,
        season: str,
        league_name: str,
        soup: BeautifulSoup
    ) -> pd.DataFrame:
        """Process match history data with additional statistics."""
        df = df.copy()
        df['team_name'] = team_name
        df['season'] = season
        df = df[df['Comp'] == league_name]
        
        # Parse additional statistics
        return self.statistics_parser.parse_statistics(soup, df)
    



class StatisticsParser:
    """Handles parsing of additional statistics tables."""
    
    def __init__(
            self, 
            config: ScraperConfig = ScraperConfig()
            ):
        self.config = config
        self.http_client = HTTPClient(retries=config.max_retries)
    
    def parse_statistics(
        self, 
        soup: BeautifulSoup, 
        base_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Parse and merge all available statistics into the base dataframe."""
        df = base_df.copy()
        anchor_links = self._extract_anchor_links(soup)
        
        for tab, columns in STATISTICS.items():
            df = self._process_statistic_table(df, tab, columns, anchor_links)
            
        return df
    
    def _extract_anchor_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract all anchor links from the page."""
        return [link.get("href") for link in soup.find_all('a') if link.get("href")]
    
    def _process_statistic_table(
        self,
        df: pd.DataFrame,
        tab: str,
        columns: Tuple[List[str], Optional[Dict[str, str]]],
        anchor_links: List[str]
    ) -> pd.DataFrame:
        """Process a single statistics table and merge it with the main dataframe."""
        try:
            # Find relevant links for this statistic
            relevant_links = [l for l in anchor_links if tab in l]
            if not relevant_links:
                return df
                
            # Fetch and process the table
            table_df = self._fetch_and_process_table(relevant_links[0], columns[0])
            if table_df is None:
                return df
                
            # Merge and rename columns if needed
            df = df.merge(table_df, on='Date', how='left')
            if columns[1]:  # If column renaming is specified
                df = self._rename_columns(df, columns[1])
                
            return df
            
        except Exception as e:
            print(f"Warning: Failed to process {tab} statistics: {str(e)}")
            return df
    
    def _fetch_and_process_table(
        self, 
        link: str, 
        columns: List[str]
    ) -> Optional[pd.DataFrame]:
        """Fetch and process a single statistics table using HTTPClient."""
        try:
            url = f"{URL_FBREF}{link}"
            response = self.http_client.get(url)
            
            # Read tables from HTML string
            tables = pd.read_html(StringIO(response.text))
            if not tables:
                return None
                
            table = tables[0]
            
            # Process table columns
            table.columns = table.columns.droplevel()
            table = table.loc[:, ~table.columns.duplicated()]
            
            # Select only needed columns
            time.sleep(self.config.request_delay)
            return table[columns]
            
        except Exception as e:
            print(f"Warning: Failed to fetch table from {link}: {str(e)}")
            return None
    
    @staticmethod
    def _rename_columns(df: pd.DataFrame, rename_map: Dict[str, str]) -> pd.DataFrame:
        """Safely rename dataframe columns."""
        try:
            return df.rename(columns=rename_map)
        except Exception as e:
            print(f"Warning: Failed to rename columns: {str(e)}")
            return df
