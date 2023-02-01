import json
import urllib
from dataclasses import dataclass


@dataclass
class SerpResponse:
    searched_results: int
    result: dict
    position: int
    domain: str
    query: str


class Serply:

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

        return SerpResponse(response)

    def get(self, url: str, data: dict, headers: dict = {}):

        request_headers = {
            'X-Api-Key': self._config.get('SERPLY_API_KEY'),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        request_headers.update(headers)

        request_url = f'{url}/{urllib.parse.urlencode(data)}'

        try:
            request = urllib.request.Request(
                url=request_url,
                headers=request_headers,
                method='GET'
            )

            content = request.urlopen(request)

            data = content.read()

            encoding = content.info().get_content_charset('utf-8')

            return json.loads(data.decode(encoding))

        except Exception as e:

            print(str(e))

            return {}
