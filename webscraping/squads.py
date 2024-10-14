import warnings
import time
import sys

import requests
import pandas as pd
from io import StringIO

from .check_seasons import CheckingSeasons
from .process_data import ProcessData
from .utils import getTeamsUrl, renameColumns, addTeamMetadata


class Squads:
    def __init__(self, countryCode) -> None:
        self.infoLeague = CheckingSeasons(countryCode, 'squads')
        self.missingSeasons = self.infoLeague.getMissingSeasons()

    def update(self) -> None:
        localFile = self.infoLeague.file
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
                localFile = pd.concat([localFile, webFile], ignore_index=True)

            except IndexError:
                warnings.warn("Error while connecting: Timeout")
                sys.exit(1)
            except Exception as e:
                self.missingSeasons.append(season)
                localFile = localFile[localFile['season'] != str(season)]
                warnings.warn(f"Error while downloading data for season {season}: {e}")
            finally:
                time.sleep(7)

        localFile.to_csv(self.infoLeague.path, index=False)
        toProcess = localFile.copy()
        ProcessData(self.infoLeague, toProcess)
