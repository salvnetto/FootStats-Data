import cloudscraper
import requests
from dataclasses import dataclass
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from cloudscraper.exceptions import CloudflareLoopProtection
from footstat.exceptions import HTTPError


@dataclass
class ScraperConfig:
    request_delay: float = 7.0
    max_retries: int = 3
    timeout: int = 10


class HTTPClient:
    def __init__(self, retries: int = 3, backoff_factor: float = 0.3):
        self.scraper = cloudscraper.create_scraper()  # Create cloudscraper instance
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        # Mount adapters to handle HTTP and HTTPS requests
        self.scraper.mount("http://", adapter)
        self.scraper.mount("https://", adapter)
    
    def get(self, url: str, timeout: int = 30) -> requests.Response:
        try:
            response = self.scraper.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (requests.RequestException, CloudflareLoopProtection) as e:
            # Extract status code if available
            response = getattr(e, 'response', None)
            status_code = response.status_code if response else None
            raise HTTPError(url, status_code)
