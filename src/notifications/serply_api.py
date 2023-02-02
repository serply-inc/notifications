import json
import urllib3
from dataclasses import dataclass, asdict

http = urllib3.PoolManager()


@dataclass
class SerpResponse:
    searched_results: int
    position: int
    domain: str
    query: str


class SerplyClient:

    _api: str = 'https://api.serply.io/v1'

    def __init__(self, config) -> None:
        self._config = config

    def serp(
        self,
        query: str,
        num: int = 100,
        domain: str = None,
        website: str = None,
    ):
        data = {
            'q': query,
            'num': num,
        }

        if domain is not None:
            data.update({domain})

        if website is not None:
            data.update({website})

        response = self.get(
            url=f'{self._api}/serp',
            data=data
        )

        return SerpResponse(
            searched_results=response.get('searched_results'),
            position=response.get('position'),
            domain=response.get('domain'),
            query=response.get('query'),
        )

    def get(self, url: str, data: dict):

        headers = {
            'X-Api-Key': self._config.get('SERPLY_API_KEY'),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        try:

            request = json.dumps(asdict(data)).encode('utf-8')

            response = http.request(
                'GET',
                url=f'{url}/{urllib3.parse.urlencode(data)}',
                body=request,
                headers=headers
            )

            return json.loads(response.data.decode('utf-8'))['json']

        except Exception as e:

            print(str(e))

            return {}
