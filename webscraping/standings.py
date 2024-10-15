import warnings
import time
import sys

import requests
import pandas as pd
from io import StringIO

from webscraping.check_seasons import CheckingSeasons
from webscraping.process_data import ProcessData
from webscraping.constants import FORMAT


class Standings:
    def __init__(self, countryCode) -> None:
        self.infoLeague = CheckingSeasons(countryCode, 'standings')
        self.missingSeasons = self.infoLeague.getMissingSeasons()

    def update(self) -> None:
        for season in self.missingSeasons:
            url = self.infoLeague.url.replace('season_placeholder', str(season))
            print(f'{self.infoLeague.leagueName} - {season} ({self.infoLeague.path})')
            try:
                data = requests.get(url)
                webFile = pd.read_html(StringIO(data.text), match=self.infoLeague.FBREFCompName)[0]
                webFile['season'] = season
                webFile['league_name'] = self.infoLeague.leagueName
                webFile['league_id'] = self.infoLeague.leagueId
                webFile.to_csv(f"{self.infoLeague.path}_{season}{FORMAT}", index=False)
            except ValueError as e:
                warnings.warn(f"Error while connecting: Timeout")
                sys.exit(1)
            except Exception as e:
                self.missingSeasons.append(season)
                warnings.warn(f"Error while downloading data for season {season}: {e}")
            finally:
                time.sleep(6.2)

        #localFile.to_csv(self.infoLeague.path, index=False)
        #toProcess = localFile.copy()
        #ProcessData(self.infoLeague, toProcess)
