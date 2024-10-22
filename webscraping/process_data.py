import os

from webscraping.leagues import League
from webscraping.utils import create_hash_key

import pandas as pd



class ProcessData:
    def __init__(self, countryCode, fileName):
        self.infoLeague = League(countryCode)
        self.fileName = fileName
        self.file = self._readFiles()

        if self.file is None or self.file.empty:
            print("No data found.")
            return

        self._ColumnsToDrop = {
            'standings': ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'],
            'match_history': ['match report', 'time', 'day'],
            'squads': ['matches']
        }
        self._processData()
    
    def _readFiles(self) -> pd.DataFrame:
        all_dfs = []
        for filename in os.listdir(self.infoLeague.path):
            if filename.endswith('.csv') and filename.startswith(f'{self.fileName}_'):
                file_path = os.path.join(self.infoLeague.path, filename)
                print(file_path)
                df = pd.read_csv(file_path)
                all_dfs.append(df)
        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            return combined_df


    def _savePath(self) -> None:
        processed_path = f'datasets/processed_data/{self.infoLeague.name}/'
        if not os.path.exists(processed_path):
            os.makedirs(os.path.dirname(processed_path))
        self.file.to_csv(processed_path + f'{self.fileName}.csv', index= False)

    def _processData(self) -> None:
        self.file.columns = self.file.columns.str.lower()
        columns_to_drop = self._ColumnsToDrop.get(self.fileName)
        self.file = self.file.drop(columns_to_drop, axis=1)
        
        if self.fileName == 'standings':
            self.file['team_id'] = self.file['squad'].apply(create_hash_key)
            
        if self.fileName == 'squads':
            self.file['age'] = self.file['age'].str.split('-').str.get(0)
            self.file = self.file.iloc[:-2]
            self.file['team_id'] = self.file['team_name'].apply(create_hash_key)

        if self.fileName == 'match_history':
            self.file = self.file[self.file['comp'] == self.infoLeague.FBREFCompName]
            self.file['round'] = self.file['round'].replace("Matchweek ", "")
            self.file['team_opp_id'] = self.file['opponent'].apply(create_hash_key)
            self.file['team_id'] = self.file['team_name'].apply(create_hash_key)

        self._savePath()