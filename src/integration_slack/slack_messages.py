from dataclasses import dataclass, field
from serply_config import SERPLY_CONFIG


@dataclass
class SerpNotificationMessage:

    blocks: list[object] = field(init=False)
    channel: str
    domain: str
    domain_or_website: str
    command: str
    interval: str
    query: str
    serp_position: int
    serp_searched_results: str
    website: str
    num: int = 100

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
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Disable',
                    },
                    'value': self.command,
                    'action_id': 'schedule.disable',
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


@dataclass
class ScheduledMessage:

    blocks: list[object] = field(init=False)
    channel: str
    domain: str
    domain_or_website: str
    command: str
    interval: str
    type: str
    query: str
    user_id: str
    website: str

    def __post_init__(self):

        self.blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\n'.join([
                        f'> *Schedule*: {self.type} {self.interval}',
                        f'> *{self.domain_or_website.title()}*: {self.domain if self.domain else self.website}',
                        f'> *Query*: {self.query}',
                    ])
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Disable',
                    },
                    'value': self.command,
                    'action_id': 'schedule.disable',
                },
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
