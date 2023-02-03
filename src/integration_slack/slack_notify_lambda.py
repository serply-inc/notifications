import json
from messages import SerpNotificationMessage
from serply_config import SERPLY_CONFIG
from serply_slack_api import SlackClient

slack = SlackClient(SERPLY_CONFIG.SLACK_BOT_TOKEN)


def handler(event, context):

    print(json.dumps(event))

    input = event.get('detail').get('input')
    notification = event.get('detail').get('notification')

    message = SerpNotificationMessage(
        channel_id=input.get('channel_id'),
        user_id=input.get('user_id'),
        domain=notification.get('domain'),
        domain_or_website=notification.get('domain_or_website'),
        interval=notification.get('interval'),
        query=notification.get('query'),
        type=notification.get('type'),
        type_name=notification.get('type_name'),
        website=notification.get('website'),
    )

    slack.notify(message)

    return {'ok': True}
