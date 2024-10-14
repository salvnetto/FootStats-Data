import os

from webscraping.utils import create_hash_key

import pandas as pd



class ProcessData:
    def __init__(self, infoLeague, file):
        self.infoLeague = infoLeague
        self.file = file
        self._ColumnsToDrop = {
        'standings': ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'],
        'match_history': ['match report', 'time', 'day'],
        'squads': ['matches']
        }
        self._processData()
    
    def _savePath(self) -> None:
        processed_path = f'datasets/processed_data/{self.infoLeague.leagueName}/'
        if not os.path.exists(processed_path):
            os.makedirs(os.path.dirname(processed_path))
        self.file.to_csv(processed_path + f'{self.infoLeague.fileName}.csv', index= False)

    def _processData(self) -> None:
        self.file.columns = self.file.columns.str.lower()
        columns_to_drop = self._ColumnsToDrop.get(self.infoLeague.fileName)
        self.file = self.file.drop(columns_to_drop, axis=1)
        
        if self.infoLeague.fileName == 'standings':
            self.file['team_id'] = self.file['squad'].apply(create_hash_key)
            
        if self.infoLeague.fileName == 'squads':
            self.file['age'] = self.file['age'].str.split('-').str.get(0)
            self.file = self.file.iloc[:-2]
            self.file['team_id'] = self.file['team_name'].apply(create_hash_key)

        if self.infoLeague.fileName == 'match_history':
            self.file = self.file[self.file['comp'] == self.infoLeague.FBREFCompName]
            self.file['round'] = self.file['round'].replace("Matchweek ", "")
            self.file['team_opp_id'] = self.file['opponent'].apply(create_hash_key)
            self.file['team_id'] = self.file['team_name'].apply(create_hash_key)

        self._savePath()