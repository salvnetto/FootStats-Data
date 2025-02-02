from typing import Dict

from footstat.exceptions import ValidationError


class LeagueValidator:
    @staticmethod
    def validate_league_config(config: Dict, country: str, league_code: str) -> None:
        if country not in config:
            available = "\n".join(f"{i}. {c}" for i, c in enumerate(config.keys(), 1))
            raise ValidationError(
                f"Invalid country '{country}'.\nAvailable countries:\n{available}"
            )
        
        if league_code not in config[country]:
            available = "\n".join(
                f"{i}. {code}" for i, code in enumerate(config[country].keys(), 1)
            )
            raise ValidationError(
                f"Invalid league code '{league_code}' for country '{country}'."
                f"\nAvailable league codes:\n{available}"
            )