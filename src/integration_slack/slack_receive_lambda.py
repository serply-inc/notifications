import json
from slack_receive_response import (
    command_response,
    default_response,
    event_response,
    interaction_response,
)


def get_challenge(body):
    if not body.startswith('{') and not body.endswith('}'):
        return False
    return json.loads(body).get('challenge', '')


responses = {
    '/slack/commands': command_response,
    '/slack/events': event_response,
    '/slack/interactions': interaction_response,
}


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

    return responses.get(event.get('path'), default_response)(event=event)
