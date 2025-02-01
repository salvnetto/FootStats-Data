import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

from exceptions import ConfigError

@dataclass
class LeagueConfig:
    country: str
    league_code: str
    name: str
    name_code: str
    id: str
    calendar: int

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.project_root = Path(__file__).parent.parent
        self.config_path = config_path or self.project_root / "database" / "leagues.json"
        
    def get_config(self) -> Dict:
        """Load and return the league configuration."""
        try:
            return json.loads(self.config_path.read_text())
        except FileNotFoundError:
            raise ConfigError(f"Config file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ConfigError(f"Invalid JSON in config file: {self.config_path}")