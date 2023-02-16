from pydash import objects
from dataclasses import dataclass, field
from serply_config import SERPLY_CONFIG

@dataclass
class ScheduleMessage:

    blocks: list[dict] = field(init=False)
    domain: str
    domain_or_website: str
    command: str
    interval: str
    type: str
    query: str
    user_id: str
    website: str
    channel: str = None
    enabled: bool = True
    replace_original: bool = False

    def __post_init__(self):
        
        action_id = SERPLY_CONFIG.EVENT_SCHEDULE_DISABLE if self.enabled else SERPLY_CONFIG.EVENT_SCHEDULE_ENABLE
        status = "enabled" if self.enabled else "disabled"

        button = {
            'type': 'button',
            'value': self.command,
            'action_id': action_id,
            'text': {
                'type': 'plain_text',
                'text': 'Disable' if self.enabled else 'Enable',
            },
        }
        
        if not self.enabled:
            button['style'] = 'primary'

        self.blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\n'.join([
                        f'> *Schedule*: {self.type} {self.interval}',
                        f'> *{self.domain_or_website.title()}*: {self.domain if self.domain else self.website}',
                        f'> *Query*: {self.query}',
                        f'> *Status*: {status}',
                    ])
                },
            },
            {
                "type": "actions",
                "elements": [button]
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f':clock1: Schedule created by <@{self.user_id}>',
                    }
                ]
            },
        ]


@dataclass
class SerpNotificationMessage:

    blocks: list[dict] = field(init=False)
    domain: str
    domain_or_website: str
    command: str
    interval: str
    query: str
    serp_position: int
    serp_searched_results: str
    website: str
    channel: str = None
    num: int = 100
    replace_original: bool = False

    def __post_init__(self):

        TEXT_ONE_TIME = f'This is a *one-time* notification.'
        TEXT_YOU_RECEIVE = f'You receive this notification *{self.interval}*. <!here>'

        website = self.domain if self.domain else self.website
        total = int(self.serp_searched_results or 0)
        google_search = f'https://www.google.com/search?q={self.query}&num={self.num}&{self.domain_or_website}={website}'
        results = f'<{google_search}|{total} results>' if total > 0 else f'0 results'

        self.blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'> `{website}` in position `{self.serp_position or 0}` for `{self.query}` from {results}.'
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f':bell: *SERP Notification* | {TEXT_ONE_TIME if self.interval in SERPLY_CONFIG.ONE_TIME_INTERVALS else TEXT_YOU_RECEIVE}'
                    }
                ]
            },
        ]
