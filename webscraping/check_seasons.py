import os
import re

import pandas as pd

from .constants import SEASONS, ACTIVE_SEASON, SUPPORTED_FILES
from .leagues import League


class CheckingSeasons:
    def __init__(self, countryCode, fileName) -> None:
        self._league = League(countryCode)
        self.downloadedSeasons = set()
        self._setProperties(fileName, countryCode)

    def _setProperties(self, fileName, countryCode) -> None:
        SUPPORTED_FILES = ['standings', 'match_history', 'squads']
        if fileName not in SUPPORTED_FILES:
            raise ValueError(f"Country Code '{countryCode}' not supported.")
      
        self.fileName = fileName
        self.path = f'{self._league.path}{self.fileName}'#.csv'
        self.url = self._league.url
        self.leagueName = self._league.name
        self.leagueId = self._league.id
        self.FBREFCompName = self._league.FBREFCompName
        
        if not os.path.exists(self._league.path):
            os.makedirs(os.path.dirname(self._league.path))
        
        for filename in os.listdir(self._league.path):
            if filename.endswith('.csv') and filename.startswith(f'{self.fileName}_'):
                match = re.search(r'standings_(\d{4})\.csv', filename)
                if match:
                    self.downloadedSeasons.add(match.group(1))
            
    def getMissingSeasons(self) -> list:
        if not self.downloadedSeasons:
            missingSeasons = SEASONS[self._league.seasonType]
        else:
            missingSeasons = [season for season in SEASONS[self._league.seasonType] if season not in self.downloadedSeasons]
            if ACTIVE_SEASON[self._league.seasonType] not in missingSeasons:
                missingSeasons.append(ACTIVE_SEASON[self._league.seasonType])

        return missingSeasons
