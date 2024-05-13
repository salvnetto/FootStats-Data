import warnings
import requests
import time

import pandas as pd
from io import StringIO

from .check_seasons import CheckingSeasons
from .process_data import ProcessData
from .utils import getTeamsUrl


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
          teamFile['season'] = season
          teamFile['league_name'] = self.infoLeague.leagueName
          teamFile['league_id'] = self.infoLeague.leagueId
          teamName = team.split('/')[-1].replace('-Stats', '').replace('-','_').lower()
          teamFile['team_name'] = teamName
          teamId = team.split('/')[5]
          teamFile['team_id'] = teamId
          print(f'--{teamName}')
          webFile.append(teamFile)
          time.sleep(1.5)
        webFile = pd.concat(webFile, ignore_index= True)
        webFile.to_excel(f'teste{season}.xlsx')
        localFile = pd.concat([localFile, webFile], ignore_index= True)

      except Exception as e:
        warnings.warn(f"Error while downloading data for season {season}: {e}")
      time.sleep(1.5)

    localFile.to_csv(self.infoLeague.path, index= False)
    ProcessData(self.infoLeague, localFile)
