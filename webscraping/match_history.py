import warnings
import requests
import time

import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

from .check_seasons import CheckingSeasons
from .process_data import ProcessData
from .utils import getTeamsUrl


class MatchHistory:
  def __init__(self, countryCode) -> None:
    self.infoLeague = CheckingSeasons(countryCode, 'match_history')
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
          teamFile = pd.read_html(StringIO(data.text))[1]
          teamFile['season'] = season
          teamFile['league_name'] = self.infoLeague.leagueName
          teamFile['league_id'] = self.infoLeague.leagueId
          teamName = team.split('/')[-1].replace('-Stats', '').replace('-','_').lower()
          teamFile['team_name'] = teamName
          teamId = team.split('/')[5]
          teamFile['team_id'] = teamId

          soup = BeautifulSoup(data.text, features= 'lxml')
          anchor = [link.get("href") for link in soup.find_all('a')]
          teamFile = self._appendOtherStats(teamFile, anchor)
          print(f'--{teamName}')
          webFile.append(teamFile)
          time.sleep(2)

        webFile = pd.concat(webFile)
        localFile = pd.concat([localFile, webFile])
      except Exception as e:
        warnings.warn(f"Error while downloading data for season {season}: {e}")
      time.sleep(2)

      localFile.to_csv(self.infoLeague.path, index= False)
      ProcessData(self.infoLeague, localFile)

  def _appendOtherStats(self, teamFile, anchor) -> pd.DataFrame:
    statsNames = {
        'all_comps/shooting/': [['Date', 'Sh', 'SoT'], []],
        'all_comps/keeper': [['Date', 'Saves'], []],
        'all_comps/passing': [['Date', 'Cmp', 'Att', 'PrgP', 'KP', '1/3'], {'1/3': 'pass_3rd'}],
        'all_comps/passing_types': [['Date', 'Sw', 'Crs'], []],
        'all_comps/gca': [['Date', 'SCA', 'GCA'], []],
        'all_comps/defense': [['Date', 'Tkl', 'TklW', 'Def 3rd', 'Att 3rd', 'Blocks', 'Int'], {'Att 3rd': 'Tkl_Att_3rd', 'Def 3rd': 'Tkl_Def_3rd'}],
        'all_comps/possession':[['Date', 'Att 3rd'], {'Att 3rd': 'Touches_Att_3rd'}],
        'all_comps/misc':[['Date', 'Fls', 'Off', 'Recov'], []]
    }

    for name, columns in statsNames.items():
      try:
        links = [l for l in anchor if l and name in l]
        webFile = pd.read_html(f"https://fbref.com{links[0]}")[0]
        webFile.columns = webFile.columns.droplevel()
        teamFile = teamFile.merge(webFile[columns[0]], on= 'Date')
        try:
          teamFile.rename(columns=columns[1], inplace=True)
        except TypeError:
          pass
      except (ValueError, IndexError, KeyError):
        pass
      time.sleep(1)
  
    return teamFile
