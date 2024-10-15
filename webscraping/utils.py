import requests
import pandas as pd
import hashlib
import unicodedata
import base64
from bs4 import BeautifulSoup


def getTeamsUrl(url) -> list:
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features='lxml')
    table = soup.select('table.stats_table')[0]
    links = table.find_all('a')
    links = [link.get('href') for link in links]
    links = [link for link in links if '/squads/' in link]
    urls = [f"https://fbref.com{link}" for link in links]

    return urls


def renameColumns(columns) -> list:
    column_counts = {}
    new_column_names = []

    for column in columns:
        if column not in column_counts:
            column_counts[column] = 1
            new_column_names.append(column)
        else:
            column_counts[column] += 1
            new_column_names.append(f"{column}_90")

    return new_column_names


def addTeamMetadata(teamFile, season, teamUrl, leagueName, leagueId, data) -> pd.DataFrame:
    teamFile['season'] = season
    teamFile['league_name'] = leagueName
    teamFile['league_id'] = leagueId
    teamName = teamUrl.split('/')[-1].replace('-Stats', '').replace('-', '_').lower()
    teamFile['team_name'] = BeautifulSoup(data.text, features='lxml').find_all('title')[0].text.split(' Stats')[0]

    print(f'--{teamName}')
    return teamFile


def create_hash_key(input_string):
    input_string = input_string.lower()
    normalized_string = unicodedata.normalize('NFD', input_string)
    input_string = ''.join(char for char in normalized_string if unicodedata.category(char) != 'Mn')
    
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))
    hash_bytes = hash_object.digest()
    hash_base64 = base64.urlsafe_b64encode(hash_bytes).decode('utf-8').rstrip('=')
    return f"{hash_base64[:9]}{input_string[:3]}"