import json
import re
from dataclasses import asdict, dataclass, field
from urllib3 import PoolManager
from serply_config import SERPLY_CONFIG


http = PoolManager()


REGEX_COMMAND_TYPE = r'(serp)'
REGEX_INTERVAL = r'(test|daily|weekly|monthly)'
REGEX_DOMAIN = r'\|([a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})>'
REGEX_WEBSITE = r'<(https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,})>'


@dataclass
class SlackCommand:
    text: str
    type: str = field(init=False)
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
        self.type = self._search(REGEX_COMMAND_TYPE, '')
        self.domain = self._search(REGEX_DOMAIN) if '|' in self.text else None
        self.website = self._search(REGEX_WEBSITE) if 'http' in self.text else None
        self.query = re.sub(r'^q=', '', self._search(rf'["\'](.*)["\']'))
        self.interval = self._search(REGEX_INTERVAL, 'daily')
        self.domain_or_website = 'domain' if self.domain else 'website'


class SlackClient:

    _api_url: str = 'https://slack.com/api/'

    def __init__(self, bot_key: str = None) -> None:
        self._bot_key = bot_key

    def notify(self, message: object):
        
        url = self._api_url + 'chat.postMessage'
        
        try:

            payload = {
                'channel': message.channel,
                'blocks': message.blocks,
            }
            
            print(payload)

            request = json.dumps(payload).encode('utf-8')

            response = http.request(
                'POST',
                url,
                body=request,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {SERPLY_CONFIG.SLACK_BOT_TOKEN}',
                }
            )

            return json.loads(response.data.decode('utf-8'))

        except Exception as e:

            print(str(e))

            return {}

    def respond(self, response_url: str, message: object):

        try:

            payload = {
                'blocks': message.blocks,
                'response_type': message.response_type,
            }

            print(payload)

            request = json.dumps(payload).encode('utf-8')

            response = http.request(
                'POST',
                response_url,
                body=request,
                headers={'Content-Type': 'application/json'}
            )

            return json.loads(response.data.decode('utf-8'))

        except Exception as e:

            print(str(e))

            return {}
