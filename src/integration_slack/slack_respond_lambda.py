import json
from slack_api import SlackClient
from slack_messages import NotificationScheduledMessage


slack = SlackClient()


def handler(event, context):
    
    print(json.dumps(event))

    # detail_type = event.get('detail-type')
    detail_notification = event.get('detail').get('notification')
    detail_input = event.get('detail').get('input')

    message = NotificationScheduledMessage(
        channel=detail_input.get('channel_id'),
        user_id=detail_input.get('user_id'),
        interval=detail_notification.get('interval'),
        type=detail_notification.get('type'),
        type_name=detail_notification.get('type_name'),
        domain=detail_notification.get('domain'),
        domain_or_website=detail_notification.get('domain_or_website'),
        query=detail_notification.get('query'),
        website=detail_notification.get('website'),
    )

    slack.respond(
        response_url=detail_input.get('response_url'),
        message=message,
    )

    return {'ok': True}
