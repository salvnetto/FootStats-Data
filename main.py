from webscraping import MatchHistory
from webscraping import Squads
from webscraping import Standings

countryCode = ['br', 'en', 'it', 'es', 'de', 'fr']

for country in countryCode:
  Standings(country).update()
  Squads(country).update()
  MatchHistory(country).update()
