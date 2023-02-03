from messages import NotificationScheduledMessage
from serply_slack_api import SlackClient

slack = SlackClient()


def handler(event, context):

    input = event.get('detail').get('input')
    notification = event.get('detail').get('notification')

    message = NotificationScheduledMessage(
        channel_id=input.get('channel_id'),
        user_id=input.get('user_id'),
        interval=notification.get('interval'),
        type=notification.get('type'),
        type_name=notification.get('type_name'),
        domain=notification.get('domain'),
        domain_or_website=notification.get('domain_or_website'),
        query=notification.get('query'),
        website=notification.get('website'),
    )
    
    slack.respond(
        response_url=input.get('response_url'), 
        message=message,
    )

    return {'ok': True}
