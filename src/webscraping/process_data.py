import os
import pandas as pd

class ProcessData:
  def __init__(self, league, file_name):
    self.league = league
    self.file_name = file_name
    self.data_frame = pd.read_csv(f'../datasets/raw_data/{self.league}/{self.file_name}.csv')
    
    self.columns_to_drop = {
      'standing': ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'],
      'match_history': ['match report', 'time', 'day']
    }


  def _save_path(self) -> None:
    processed_path = f'../datasets/processed_data/{self.league}/'
    if not os.path.exists(processed_path):
      os.makedirs(processed_path)
    
    self.data_frame.to_csv(processed_path + f'{self.file_name}.csv')


  def process_data(self) -> None:
    self.data_frame.columns = self.data_frame.columns.str.lower()
    columns_to_drop = self.columns_to_drop.get(self.file_name, [])
    self.data_frame = self.data_frame.drop(columns_to_drop, axis=1)

    self._save_path()