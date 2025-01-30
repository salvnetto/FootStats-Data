from typing import List, Tuple
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

from exceptions import ParsingError



class DataParser:
    @staticmethod
    def parse_team_urls(html_content: str) -> List[str]:
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

    @staticmethod
    def parse_team_data(
        html_content: str, 
        team_name: str, 
        league_name: str, 
        season: str
        ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Parse squad and match history data from team page."""
        try:
            tables = pd.read_html(StringIO(html_content))
            
            # Process squad data
            squad_df = tables[0]
            squad_df['team_name'] = team_name
            squad_df['season'] = season
            
            # Process match history
            match_history_df = tables[1]
            match_history_df['team_name'] = team_name
            match_history_df['season'] = season
            match_history_df = match_history_df[match_history_df['Comp'] == league_name]
            
            return squad_df, match_history_df
        except Exception as e:
            raise ParsingError(f"Failed to parse team data: {str(e)}")
