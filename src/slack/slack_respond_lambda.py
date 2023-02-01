import json
from slack import SlackClient, SlackCommand

client = SlackClient()


def handler(event, context):
    print(json.dumps(event))

    data = event.get('detail').get('data')
    response_url = data.get('response_url')
    command = SlackCommand(data.get('text'))

    blocks = [
        {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': f'{command.type_name} Notification Scheduled {command.interval.title()}',
                'emoji': True
            }
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f'*type:* {command.type}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*{command.domain_or_website}:* {command.domain if command.domain else command.website}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*query:* {command.query}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*interval:* {command.interval}'
                },
            ]
        },
    ]

    client.post(response_url, {
        'blocks': blocks,
        'response_type': 'in_channel',
    })

    return {'ok': True}
