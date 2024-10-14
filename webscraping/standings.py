import warnings
import time
import sys

import requests
import pandas as pd
from io import StringIO

from .check_seasons import CheckingSeasons
from .process_data import ProcessData


class Standings:
    def __init__(self, countryCode) -> None:
        self.infoLeague = CheckingSeasons(countryCode, 'standings')
        self.missingSeasons = self.infoLeague.getMissingSeasons()

    def update(self) -> None:
        localFile = self.infoLeague.file
        for season in self.missingSeasons:
            url = self.infoLeague.url.replace('season_placeholder', str(season))
            print(f'{self.infoLeague.leagueName} - {season} ({self.infoLeague.path})')
            try:
                data = requests.get(url)
                webFile = pd.read_html(StringIO(data.text), match=self.infoLeague.FBREFCompName)[0]
                webFile['season'] = season
                webFile['league_name'] = self.infoLeague.leagueName
                webFile['league_id'] = self.infoLeague.leagueId
                #localFile = pd.concat([localFile, webFile], ignore_index=True)
            except ValueError as e:
                warnings.warn(f"Error while connecting: Timeout")
                sys.exit(1)
            except Exception as e:
                self.missingSeasons.append(season)
                #localFile = localFile[localFile['season'] != str(season)]
                warnings.warn(f"Error while downloading data for season {season}: {e}")
            finally:
                time.sleep(7)

        localFile.to_csv(self.infoLeague.path, index=False)
        toProcess = localFile.copy()
        ProcessData(self.infoLeague, toProcess)
