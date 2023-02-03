import json
from random import randint
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib3 import PoolManager


http = PoolManager()


@dataclass
class SerpResponse:
    searched_results: int
    position: int
    domain: str
    query: str
    title: str
    link: str
    description: str


class SerplyClient:

    _api: str = 'https://api.serply.io/v1'
    _api_key: str = None

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def serp(
        self,
        query: str,
        domain: str = None,
        website: str = None,
        num: int = 100,
        mock: bool = False,
    ):
        if mock:
            return self.serpMock(
                query=query,
                domain=domain,
                website=website,
            )
        
        if domain is None and website is None:
            raise Exception('SerplyClient.serp: domain or website required.')

        data = {
            'q': query,
            'num': num,
        }

        if domain is not None:
            data['domain'] = domain

        if website is not None:
            data['website'] = website

        response = self.get(
            path='serp',
            data=data
        )

        return SerpResponse(
            searched_results=response.get('searched_results'),
            position=response.get('position'),
            domain=response.get('domain'),
            query=response.get('query'),
            title=response.get('result').get('title'),
            description=response.get('result').get('description'),
            link=response.get('result').get('link'),
        )

    def serpMock(
        self,
        query: str,
        domain: str = None,
        website: str = None,
    ):
        return SerpResponse(
            searched_results=randint(75, 100),
            position=randint(15, 50),
            domain=domain if domain else website,
            query=query,
            title='Test title for SERP mock response',
            description='Test description for SERP mock response',
            link='https://example.com/',
        )

    def get(self, path: str, data: dict):

        if self._api_key is None:
            raise Exception('SERPLY_API_KEY required.')

        headers = {
            'X-Api-Key': self._api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        try:

            body = json.dumps(data).encode('utf-8')

            url = f'{self._api}/{path}/{urlencode(data)}'

            response = http.request(
                'GET',
                url=url,
                body=body,
                headers=headers
            )

            return json.loads(response.data.decode('utf-8'))

        except Exception as e:

            print(str(e))

            return {}
