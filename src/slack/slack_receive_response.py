import boto3
import json
from serply_config import SERPLY_CONFIG
from serply_database import schedule_from_dict
from serply_events import EventBus
from slack_api import SlackCommand
from urllib.parse import parse_qs
from pydash import objects

event_bus = EventBus(boto3.client('events'))


def get(data: dict, key: str):
    return data.get(key)[0] if type(data.get(key)) == list and len(data.get(key)) > 0 else data.get(key)


def querystring_asdict(querystring: str):
    values = dict()
    input = parse_qs(querystring)
    for key in input.keys():
        values[key] = get(input, key)
    return values


def default_response(event={}):
    return {
        'statusCode': 200,
        'body': '{}',
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def command_response(event={}):
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

    headers = event.get('headers')
    input = querystring_asdict(event.get('body'))
    command = SlackCommand(command=input.get('text'))

    # @todo validated signature or raise exception

    if command.type == 'list':
        event_bus.put(
            source=SERPLY_CONFIG.EVENT_SOURCE_SLACK,
            detail_type=SERPLY_CONFIG.EVENT_SCHEDULE_LIST,
            schedule=command,
            input=input,
            headers=headers,
        )
    else:
        event_bus.put(
            source=SERPLY_CONFIG.EVENT_SOURCE_SLACK,
            detail_type=SERPLY_CONFIG.EVENT_SCHEDULE_SAVE,
            schedule=command,
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


def event_response(event={}):
    return default_response(event)


def interaction_response(event={}):

    # def disable(payload={}, value=None):
    #     print('run disable()')
    #     return {
    #         'statusCode': 200,
    #         'body': json.dumps({
    #             "text": "Disabled!",
    #             "response_type": "in_channel",
    #             "replace_original": "true",
    #         }),
    #         'headers': {
    #             'Content-Type': 'application/json',
    #         }
    #     }

    # def default(payload={}, value=None):
    #     return {
    #         'statusCode': 200,
    #         'body': '',
    #         'headers': {
    #             'Content-Type': 'text/plain',
    #         },
    #     }

    # actions = {
    #     'disable': disable,
    # }
    
    headers = event.get('headers')
    
    body = querystring_asdict(event.get('body'))
    payload = json.loads(body.get('payload'))
    action = objects.get(payload, 'actions[0].action_id')
    command = objects.get(payload, 'actions[0].value')

    schedule = SlackCommand(command=command)

    if action not in [
        SERPLY_CONFIG.EVENT_SCHEDULE_DISABLE,
        SERPLY_CONFIG.EVENT_SCHEDULE_ENABLE,
    ]:
        raise Exception(f'Invalid action: {action}')

    event_bus.put(
        source=SERPLY_CONFIG.EVENT_SOURCE_SLACK,
        detail_type=action,
        schedule=schedule,
        input=payload,
        headers=headers,
    )

    return {
        'statusCode': 200,
        'body': '{}',
        'headers': {
            'Content-Type': 'application/json',
        },
    }
