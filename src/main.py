from webscraping.scrap_leagues import GetData

league_list = ['br', 'en', 'it', 'es', 'de', 'fr']

for league in league_list:
  if league == 'br':
    league = GetData(league)
  else:
    league = GetData(league)
  
  #league.get_standings()
  league.get_match_history()
  #league.get_squads(has_downloaded=False)
  #league.get_squads(has_downloaded=True)
