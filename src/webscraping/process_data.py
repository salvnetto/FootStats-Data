import os
import pandas as pd

class ProcessData:
  def __init__(self, league, fileName):
    self._league = league
    self._fileName = fileName
    self._dataFrame = pd.read_csv(f'../datasets/raw_data/{self._league}/{self._fileName}.csv')
    
    self._ColumnsToDrop = {
      'standing': ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'],
      'match_history': ['match report', 'time', 'day']
    }

    self._processData()
   
  def _savePath(self) -> None:
    processed_path = f'../datasets/processed_data/{self._league}/'
    if not os.path.exists(processed_path):
      os.makedirs(processed_path)
    
    self._dataFrame.to_csv(processed_path + f'{self._fileName}.csv')


  def _processData(self) -> None:
    self._dataFrame.columns = self._dataFrame.columns.str.lower()
    columns_to_drop = self._ColumnsToDrop.get(self._fileName, [])
    self._dataFrame = self._dataFrame.drop(columns_to_drop, axis=1)

    self._savePath()