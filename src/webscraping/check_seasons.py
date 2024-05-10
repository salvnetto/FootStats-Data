import os
import pandas as pd

from .constants import SEASONS
from .leagues import League


class CheckingSeasons:
  def __init__(self, countryCode, fileName) -> None:
    self.league = League(countryCode)
    self._setProperties(fileName, countryCode)
    

  def _setProperties(self, fileName, countryCode) -> None:
    files = ['standings', 'match_history', 'squads']
    if fileName in files:
      self.fileName = fileName
      self.path = f'{self.league.path}{self.fileName}.csv'
    else:
      raise ValueError(f"Country Code '{countryCode}' not supported.")
  
    if not os.path.exists(self.path):
      self.file = pd.DataFrame()
      self.file.to_csv(self.path)
    else:
      self.file = pd.read_csv(self.path)
      
  def getDownloadedSeasons(self) -> list:
    ...
