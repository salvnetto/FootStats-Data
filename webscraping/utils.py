import requests
import re
import pandas as pd
import hashlib
import unicodedata
import base64
from bs4 import BeautifulSoup

NAME_CHANGES = {
    "Ath Paranaense": "Athletico Paranaense",
    "Atl Goianiense": "Atlético Goianiense"
}

def create_hash_key(input_string):
    input_string = input_string.lower()
    normalized_string = unicodedata.normalize('NFD', input_string)
    input_string = ''.join(char for char in normalized_string if unicodedata.category(char) != 'Mn')
    
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))
    hash_bytes = hash_object.digest()
    hash_base64 = base64.urlsafe_b64encode(hash_bytes).decode('utf-8').rstrip('=')
    return f"{hash_base64[:9]}{input_string[:3]}"

def remove_numbers_from_string(text):
    return re.sub(r'^\d{4}\s+', '', text)

def change_opponent(team_name):
    return NAME_CHANGES.get(team_name, team_name)