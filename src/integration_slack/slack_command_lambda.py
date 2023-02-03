import boto3
import json
from serply_events import NotificationEventBus
from slack_api import SlackCommand
from urllib.parse import parse_qs


notification_event_bus = NotificationEventBus(boto3.client('events'))


def validate_command(command):

    # valid_commands = ['serp']

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
    return data.get(key)[0] if type(data.get(key)) == list and len(data.get(key)) > 0 else data.get(key)


def querystring_asdict(querystring: str):
    values = dict()
    input = parse_qs(querystring)
    for key in input.keys():
        values[key] = get(input, key)
    return values


def handler(event, context):
    
    print(json.dumps(event))
    
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
    input = querystring_asdict(event.get('body'))
    notification = SlackCommand(text=input.get('text'))

    # @todo validated signature or raise exception
    
    notification_event_bus.put(
        notification=notification,
        input=input,
        headers=headers,
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'response_type': 'in_channel',
        }),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
