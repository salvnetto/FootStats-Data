import warnings
import time
import sys

import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

from webscraping.check_seasons import CheckingSeasons
from webscraping.process_data import ProcessData
from webscraping.utils import getTeamsUrl, addTeamMetadata
from webscraping.constants import FORMAT


class MatchHistory:
    def __init__(self, countryCode) -> None:
        self.infoLeague = CheckingSeasons(countryCode, 'match_history')
        self.missingSeasons = self.infoLeague.getMissingSeasons()

    def update(self) -> None:
        for season in self.missingSeasons:
            url = self.infoLeague.url.replace('season_placeholder', str(season))
            print(f'{self.infoLeague.leagueName} - {season} ({self.infoLeague.path})')
            try:
                teamsUrls = getTeamsUrl(url)
                webFile = []
                for team in teamsUrls:
                    data = requests.get(team)
                    teamFile = pd.read_html(StringIO(data.text))[1]
                    teamFile = addTeamMetadata(
                        teamFile, season, team, self.infoLeague.leagueName, self.infoLeague.leagueId, data
                    )

                    soup = BeautifulSoup(data.text, features='lxml')
                    anchor = [link.get("href") for link in soup.find_all('a')]
                    teamFile = self._appendOtherStats(teamFile, anchor)
                    
                    webFile.append(teamFile)
                    time.sleep(7)

                webFile = pd.concat(webFile)
                webFile.to_csv(f"{self.infoLeague.path}_{season}{FORMAT}", index=False)
            except IndexError:
                warnings.warn("Error while connecting: Timeout")
                sys.exit(1)
            except Exception as e:
                self.missingSeasons.append(season)
                warnings.warn(f"Error while downloading data for season {season}: {e}")
            finally:
                time.sleep(7)


    def _appendOtherStats(self, teamFile, anchor) -> pd.DataFrame:
        statsNames = {
            'all_comps/shooting/': [
                ['Date', 'Sh', 'SoT', 'SoT%', 'G/Sh', 'G/SoT', 'Dist'], []
            ],
            'all_comps/keeper': [
                ['Date', 'SoTA', 'Saves', 'Save%', 'PSxG', 'PSxG+/-'], []
            ],
            'all_comps/passing': [
                ['Date', 'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist', 'Ast', 'xAG', 'xA', 'CrsPA', 'PrgP', 'KP', '1/3'], {'1/3': 'pass_3rd'}
            ],
            'all_comps/passing_types': [
                ['Date', 'Sw', 'Crs', 'TB', 'CK'], []
            ],
            'all_comps/gca': [
                ['Date', 'SCA', 'GCA'], []
            ],
            'all_comps/defense': [
                ['Date', 'Tkl', 'TklW', 'Def 3rd', 'Att 3rd', 'Blocks', 'Int', 'Clr', 'Err'], {'Att 3rd': 'Tkl_Att_3rd', 'Def 3rd': 'Tkl_Def_3rd'}
            ],
            'all_comps/possession': [
                ['Date', 'Att 3rd', 'PrgC', '1/3', 'Mis', 'Dis'], {'Att 3rd': 'Touches_Att_3rd', '1/3': 'Carries_Att_3rd'}
            ],
            'all_comps/misc': [
                ['Date', 'Fls', 'Off', 'Recov', 'Won%'], []
            ]
        }

        for name, columns in statsNames.items():
            try:
                links = [l for l in anchor if l and name in l]
                webFile = pd.read_html(f"https://fbref.com{links[0]}")[0]
                webFile.columns = webFile.columns.droplevel()
                webFile = webFile.loc[:, ~webFile.columns.duplicated()]
                teamFile = teamFile.merge(webFile[columns[0]], on='Date')
                try:
                    teamFile.rename(columns=columns[1], inplace=True)
                except TypeError:
                    pass
            except (ValueError, IndexError, KeyError):
                pass
            time.sleep(7)
        return teamFile
