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
    type_name: str
    query: str
    user_id: str
    website: str
    serp_searched_results: str
    serp_domain: str
    serp_query: str
    serp_title: str
    serp_link: str
    serp_description: str

    def __post_init__(self):

        self.blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'SERP {self.interval.title()} Notification',
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'{self.domain if self.domain else self.website} has position {self.serp_position} for "{self.query} from {self.serp_searched_results} searched results."'
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*title:* {self.serp_title}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*description:* {self.serp_description}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*domain:* {self.serp_domain}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*serp:* {self.serp_query}'
                    },
                ]
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
    type_name: str
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
                    'text': f'{self.type_name} Notification Scheduled {self.interval.title()}',
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f'*by:* <@{self.user_id}>',
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*channel:* <#{self.channel}>'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*type:* {self.type}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*{self.domain_or_website}:* {self.domain if self.domain else self.website}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*query:* {self.query}'
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f'*interval:* {self.interval}'
                    },
                ]
            },
        ]
