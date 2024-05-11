import os
import pandas as pd

class ProcessData:
  def __init__(self, infoLeague, file):
    self.infoLeague = infoLeague
    self.file = file
    self._ColumnsToDrop = {
      'standings': ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'],
      'match_history': ['match report', 'time', 'day']
    }
    self._processData()
   
  def _savePath(self) -> None:
    processed_path = f'datasets/processed_data/{self.infoLeague.leagueName}/'
    if not os.path.exists(processed_path):
      os.makedirs(os.path.dirname(processed_path)
    self.file.to_csv(processed_path + f'{self.infoLeague.fileName}.csv', index= False)

  def _processData(self) -> None:
    self.file.columns = self.file.columns.str.lower()
    columns_to_drop = self._ColumnsToDrop.get(self.infoLeague.fileName)
    self.file = self.file.drop(columns_to_drop, axis=1)
    self._savePath()