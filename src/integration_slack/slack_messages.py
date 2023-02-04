from dataclasses import dataclass, field


@dataclass
class SerpNotificationMessage:

    blocks: list[object] = field(init=False)
    serp_position: int
    channel: str
    domain: str
    domain_or_website: str
    interval: str
    type: str
    query: str
    user_id: str
    website: str
    serp_searched_results: str
    serp_domain: str
    serp_query: str

    def __post_init__(self):

        TEXT_ONE_TIME = f'This is a *one-time* response.'
        TEXT_YOU_RECEIVE = f'You receive this notification *{self.interval}*.'

        self.blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'> {self.domain if self.domain else self.website} in position `{self.serp_position}` for `{self.query}` from `{self.serp_searched_results}` results.'
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Disable',
                    },
                    'value': 'schedule_hash',
                    'action_id': 'disable',
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*SERP Notification* | {TEXT_ONE_TIME if self.interval in ["once", "mock"] else TEXT_YOU_RECEIVE}'
                    }
                ]
            },
            {
                'type': 'divider'
            },
        ]


@dataclass
class NotificationScheduledMessage:

    blocks: list[object] = field(init=False)
    channel: str
    domain: str
    domain_or_website: str
    interval: str
    type: str
    query: str
    user_id: str
    website: str
    response_type: str = 'in_channel'

    def __post_init__(self):

        self.blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f'SERP Schedule Configured',
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\n'.join([
                        f'*{self.domain_or_website}:* {self.domain if self.domain else self.website}',
                        f'*query:* `{self.query}`',
                        f'*interval:* `{self.interval}`',
                    ])
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Disable',
                    },
                    'value': 'schedule_hash',
                    'action_id': 'disable',
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'Configured by <@{self.user_id}> in <#{self.channel}>'
                    }
                ]
            },
            {
                'type': 'divider'
            },
        ]
