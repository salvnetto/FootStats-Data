import os
import pandas as pd

from .constants import SEASONS


class CheckingSeasons:
  def __init__(self, league) -> None:
    self.league = league
    self.downloadedSeasons = list()
    self.file = pd.DataFrame()
    self.hasDataframe = bool

  def checkDataframe(self):
    if not os.path.exists():
      ...