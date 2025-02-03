import json

from footstat import LeagueDataManager


def main_function():
    path = "database/leagues.json"
    with open(path, "r") as file:
        data = json.load(file)


    for country, leagues in data.items():
        for league, value in leagues.items():
            LeagueDataManager(country, league)
    
if __name__ == "__main__":
    main_function()
