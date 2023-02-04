import json
from slack_api import SlackClient
from slack_messages import NotificationScheduledMessage
from serply_database import notification_from_dict


slack = SlackClient()


def handler(event, context):
    
    print(json.dumps(event))

    # detail_type = event.get('detail-type')
    detail_input = event.get('detail').get('input')
    notification = notification_from_dict(event.get('detail').get('notification'))

    message = NotificationScheduledMessage(
        channel=detail_input.get('channel_id'),
        user_id=detail_input.get('user_id'),
        interval=notification.interval,
        type=notification.type,
        domain=notification.domain,
        domain_or_website=notification.domain_or_website,
        query=notification.query,
        website=notification.website,
    )

    slack.respond(
        response_url=detail_input.get('response_url'),
        message=message,
    )

    return {'ok': True}
