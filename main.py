import webscraping as ws

countryCode = ['br', 'en', 'it', 'es', 'de', 'fr'] #

for country in countryCode:
  ws.MatchHistory(country).update()
  ws.Standings(country).update()
  ws.Squads(country).update()
