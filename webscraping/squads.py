import warnings
import time
import sys

import requests
import pandas as pd
from io import StringIO

from webscraping.check_seasons import CheckingSeasons
from webscraping.process_data import ProcessData
from webscraping.utils import getTeamsUrl, renameColumns, addTeamMetadata
from webscraping.constants import FORMAT


class Squads:
    def __init__(self, countryCode) -> None:
        self.infoLeague = CheckingSeasons(countryCode, 'squads')
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
                    teamFile = pd.read_html(StringIO(data.text))[0]
                    teamFile.columns = teamFile.columns.droplevel()
                    teamFile = addTeamMetadata(
                        teamFile, season, team, self.infoLeague.leagueName, self.infoLeague.leagueId, data
                    )
                    teamFile.columns = renameColumns(teamFile.columns)
                    webFile.append(teamFile)
                    time.sleep(7)
                webFile = pd.concat(webFile, ignore_index=True)
                webFile.to_csv(f"{self.infoLeague.path}_{season}{FORMAT}", index=False)
            except IndexError:
                warnings.warn("Error while connecting: Timeout")
                sys.exit(1)
            except Exception as e:
                self.missingSeasons.append(season)
                warnings.warn(f"Error while downloading data for season {season}: {e}")
            finally:
                time.sleep(7)

