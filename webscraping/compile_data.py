import os

import pandas as pd

from webscraping.constants import SUPPORTED_FILES, FORMAT
from webscraping.leagues import League

def CompileData(country_code):
    league = League(country_code).name
    input_folder_path = f'datasets\\raw_data\\{league}'
    output_folder_path = f'datasets\\processed_data\\{league}'

    for SUPPORTED_FILE in SUPPORTED_FILES:
        all_files = [f for f in os.listdir(input_folder_path) if f.startswith(SUPPORTED_FILE) and f.endswith(FORMAT)]

        dataframes = []
        for file in all_files:
            file_path = os.path.join(input_folder_path, file)
            df = pd.read_csv(file_path)
            dataframes.append(df)
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        concatenated_df.to_csv(f'{output_folder_path}/{SUPPORTED_FILE}{FORMAT}', index=False)

