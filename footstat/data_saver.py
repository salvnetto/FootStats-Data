from pathlib import Path
import pandas as pd



class DataSaver:
    def __init__(self, base_path: str, league_code: str):
        self.base_path = Path(base_path) / "raw_data" / league_code
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_season_data(self, squad_df: pd.DataFrame, match_history_df: pd.DataFrame, season: str) -> None:
        """Save season data to CSV files."""
        squad_df.to_csv(self.base_path / f"squad_{season}.csv", index=False)
        match_history_df.to_csv(self.base_path / f"match_history_{season}.csv", index=False)

