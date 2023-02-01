from dataclasses import dataclass, field


@dataclass
class NotificationScheduledMessage:

    blocks: list[object] = field(init=False)
    channel_id: str
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
                        'text': f'*channel:* <#{self.channel_id}>'
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
