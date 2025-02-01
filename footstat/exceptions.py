from typing import Optional



# league_manager
class LeagueManagerError(Exception):
    """Base exception for the league manager module."""
    pass

class ConfigError(LeagueManagerError):
    """Configuration related errors."""
    pass

class ValidationError(LeagueManagerError):
    """Validation related errors."""
    pass



# scraper
class ScraperError(Exception):
    """Base exception for scraping operations."""
    pass

class HTTPError(ScraperError):
    """Raised when HTTP requests fail."""
    def __init__(self, url: str, status_code: Optional[int] = None):
        self.url = url
        self.status_code = status_code
        super().__init__(f"Failed to fetch {url}" + 
                        f" (Status: {status_code})" if status_code else "")

class ParsingError(ScraperError):
    """Raised when parsing operations fail."""
    pass