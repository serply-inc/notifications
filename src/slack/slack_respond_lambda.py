import json
from api import SlackClient

slack = SlackClient()


def handler(event, context):
    print(json.dumps(event))

    detail = event.get('detail')
    
    # Event detail
    response_url = detail.get('response_url')
    user_id = detail.get('user_id')
    channel_id = detail.get('channel_id')
    command = detail.get('command')
    
    # Command parameters
    type = command.get('type')
    type_name = command.get('type_name')
    interval = command.get('interval')
    domain_or_website = command.get('domain_or_website')
    domain = command.get('domain')
    website = command.get('website')
    query = command.get('query')

    blocks = [
        {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': f'{type_name} Notification Scheduled {interval.title()}',
                'emoji': True
            }
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f'*by:* <@{user_id}>'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*channel:* <#{channel_id}>'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*type:* {type}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*{domain_or_website}:* {domain if domain else website}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*query:* {query}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*interval:* {interval}'
                },
            ]
        },
    ]

    slack.post(response_url, {
        'blocks': blocks,
        'response_type': 'in_channel',
    })

    return {'ok': True}
