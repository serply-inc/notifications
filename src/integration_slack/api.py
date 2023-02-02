import json
import re
import urllib3
from dataclasses import asdict, dataclass, field, is_dataclass

http = urllib3.PoolManager()


REGEX_COMMAND_TYPE = r'(serp)'
REGEX_INTERVAL = r'(test|daily|weekly|monthly)'
REGEX_DOMAIN = r'\|([a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})>'
REGEX_WEBSITE = r'<(https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})>'


@dataclass
class SlackCommand:
    text: str
    type: str = field(init=False)
    type_name: str = field(init=False)
    website: str = field(init=False)
    domain: str = field(init=False)
    query: str = field(init=False)
    interval: str = field(init=False)
    domain_or_website: str = field(init=False)

    def _search(self, pattern, default_value=None):
        match = re.search(pattern, self.text)
        if match:
            return match[1] if match.lastindex and match.lastindex >= 1 else default_value
        return default_value

    def __post_init__(self):
        type_name_map = {'serp': 'SERP'}
        self.type = self._search(REGEX_COMMAND_TYPE, '')
        self.type_name = type_name_map.get(self.type)
        self.domain = self._search(REGEX_DOMAIN) if '|' in self.text else None
        self.website = self._search(REGEX_WEBSITE) if 'http' in self.text else None
        self.query = re.sub(r'^q=', '', self._search(rf'["\'](.*)["\']'))
        self.interval = self._search(REGEX_INTERVAL, 'daily')
        self.domain_or_website = 'domain' if self.domain else 'website'


class SlackClient:

    def post(self, url: str, data: dict):

        try:

            request = json.dumps(asdict(data)).encode('utf-8')

            response = http.request(
                'POST',
                url,
                body=request,
                headers={'Content-Type': 'application/json'}
            )

            return json.loads(response.data.decode('utf-8'))['json']

        except Exception as e:

            print(str(e))

            return {}
