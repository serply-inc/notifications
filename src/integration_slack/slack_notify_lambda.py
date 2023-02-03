import json
from serply_config import SERPLY_CONFIG
from slack_api import SlackClient
from slack_messages import SerpNotificationMessage


slack = SlackClient(SERPLY_CONFIG.SLACK_BOT_TOKEN)


def handler(event, context):

    print(json.dumps(event))

    # detail_type = event.get('detail-type')
    detail_notification = event.get('detail').get('notification')
    detail_input = event.get('detail').get('input')

    message = SerpNotificationMessage(
        channel_id=detail_input.get('channel_id'),
        user_id=detail_input.get('user_id'),
        domain=detail_notification.get('domain'),
        domain_or_website=detail_notification.get('domain_or_website'),
        interval=detail_notification.get('interval'),
        query=detail_notification.get('query'),
        type=detail_notification.get('type'),
        type_name=detail_notification.get('type_name'),
        website=detail_notification.get('website'),
    )

    slack.notify(message)

    return {'ok': True}
