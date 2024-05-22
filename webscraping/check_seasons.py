import os

import pandas as pd

from .constants import SEASONS, ACTIVE_SEASON
from .leagues import League


class CheckingSeasons:
    def __init__(self, countryCode, fileName) -> None:
        self._league = League(countryCode)
        self._setProperties(fileName, countryCode)

    def _setProperties(self, fileName, countryCode) -> None:
        supportedFiles = ['standings', 'match_history', 'squads']
        if fileName not in supportedFiles:
            raise ValueError(f"Country Code '{countryCode}' not supported.")
      
        self.fileName = fileName
        self.path = f'{self._league.path}{self.fileName}.csv'
        self.url = self._league.url
        self.leagueName = self._league.name
        self.leagueId = self._league.id
        self.FBREFCompName = self._league.FBREFCompName
        
        if not os.path.exists(self._league.path):
            os.makedirs(os.path.dirname(self._league.path))
        
        if not os.path.exists(self.path):
            self.file = pd.DataFrame({'season': []})
            self.file.to_csv(self.path, index= False)
        else:
            self.file = pd.read_csv(self.path)
            self.file['season'] = self.file['season'].apply(str)
            self.file = self.file[self.file['season'] != ACTIVE_SEASON[self._league.seasonType]]
            
    def getMissingSeasons(self) -> list:
        downloadedSeasons = list(self.file['season'].unique())
        downloadedSeasons = [str(season) for season in downloadedSeasons]

        if not downloadedSeasons:
            missingSeasons = SEASONS[self._league.seasonType]
        else:
            missingSeasons = [season for season in SEASONS[self._league.seasonType] if season not in downloadedSeasons]
            if ACTIVE_SEASON[self._league.seasonType] not in missingSeasons:
                missingSeasons.append(ACTIVE_SEASON[self._league.seasonType])

        return missingSeasons
