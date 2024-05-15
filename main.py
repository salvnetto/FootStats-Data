import webscraping as ws

countryCode = ['br', 'en', 'it', 'es', 'de', 'fr']

for country in countryCode:
  ws.Standings(country).update()
  #ws.Squads(country).update()
  ws.MatchHistory(country).update()
