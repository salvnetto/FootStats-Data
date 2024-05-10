from .constants import *

class League:
  def __init__(self, countryCode):
    self.countryCode = countryCode
    
  def _setLeagueProperties(self): 
    leagues = {
      'br': ('brasileirao', '24', 'full_year'),
      'en': ('premier_league', '9', 'split_years'),
      'it': ('serie_a', '11', 'split_years'),
      'es': ('la_liga', '12', 'split_years'),
      'de': ('bundesliga', '20', 'split_years'),
      'fr': ('ligue_1', '13', 'split_years')
    }

    if self.countryCode in leagues:
      self.name, self.id, self.seasonType = leagues[self.league]

      _urlName = self.name.replace('_','-').title()
      self.url = f"{URL_FBREF}/en/comps/{self.league_id}/season_placeholder/season_placeholder-{_urlName}-Stats"

      self.path = f"datasets/raw_data/{self.name}/"