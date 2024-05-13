import warnings
import requests
import time

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
        webFile = pd.read_html(StringIO(data.text), match='Regular season')[0]
        webFile['season'] = season
        webFile['league_name'] = self.infoLeague.leagueName
        webFile['league_id'] = self.infoLeague.leagueId
        localFile = pd.concat([localFile, webFile])
      except Exception as e:
        warnings.warn(f"Error while downloading data for season {season}: {e}")
      time.sleep(2)

    localFile.to_csv(self.infoLeague.path, index= False)
    ProcessData(self.infoLeague, localFile)
