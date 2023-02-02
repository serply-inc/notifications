import boto3
import json
from api import SlackCommand
from dataclasses import asdict
from os import getenv
from urllib.parse import parse_qs

STAGE = getenv("STAGE", 'dev')

events = boto3.client('events')


def validate_command(command):

    valid_commands = ['serp']

    # if parser.type not in valid_commands:
    #     ack(
    #         f'Please enter a valid command. Example: {COMMAND} serp google.com "google+search+api" daily')
    #     return
    # elif parser.query == None:
    #     ack('A query is required in single or double quotes.')
    #     return
    # else:
    #     ack()
    pass


def get_challenge(body):
    if not body.startswith('{') and not body.endswith('}'):
        return False
    return json.loads(body).get('challenge', '')


def get(data: dict, key: str):
    return data.get(key)[0] if type(data.get(key)) == list else data.get(key)


def handler(event, context):
    challenge = get_challenge(event.get('body'))

    if challenge:
        return {
            'statusCode': 200,
            'body': challenge,
            'headers': {
                'Content-Type': 'text/plain',
            },
        }

    headers = event.get('headers')
    data = parse_qs(event.get('body'))
    command = SlackCommand(text=get(data, 'text'))

    print(command)

    event = {
        'Source': 'serply',
        'DetailType': command.type,
        'Resources': [],
        'Detail': json.dumps({
            'provider': 'slack',
            'text': get(data, 'text'),
            'team_id': get(data, 'team_id'),
            'team_domain': get(data, 'team_domain'),
            'channel_id': get(data, 'channel_id'),
            'channel_name': get(data, 'channel_name'),
            'user_id': get(data, 'user_id'),
            'user_name': get(data, 'user_name'),
            'api_app_id': get(data, 'api_app_id'),
            'response_url': get(data, 'response_url'),
            'trigger_id': get(data, 'trigger_id'),
            'stage': STAGE,
            'command': asdict(command),
            'headers': {
                'X-Amzn-Trace-Id': headers.get('X-Amzn-Trace-Id'),
                'X-Slack-Request-Timestamp': headers.get('X-Slack-Request-Timestamp'),
                'X-Slack-Signature': headers.get('X-Slack-Signature'),
            }
        }),
        'EventBusName': f'NotificationsEventBus{STAGE.title()}',
        'TraceHeader': headers.get('X-Amzn-Trace-Id')
    }
    
    print(event)

    # @todo validated signature or raise exception

    put_events_response = events.put_events(Entries=[event])
    
    print(put_events_response)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'response_type': 'in_channel',
        }),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
