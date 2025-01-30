import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from exceptions import HTTPError



class HTTPClient:
    def __init__(self, retries: int = 3, backoff_factor: float = 0.3):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get(self, url: str, timeout: int = 30) -> requests.Response:
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise HTTPError(url, getattr(e.response, 'status_code', None))