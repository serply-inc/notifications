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
        channel=detail_input.get('channel_id'),
        user_id=detail_input.get('user_id'),
        domain=detail_notification.get('domain'),
        domain_or_website=detail_notification.get('domain_or_website'),
        interval=detail_notification.get('interval'),
        query=detail_notification.get('query'),
        type=detail_notification.get('type'),
        website=detail_notification.get('website'),
        serp_position=detail_notification.get('serp_position'),
        serp_searched_results=detail_notification.get('serp_searched_results'),
        serp_domain=detail_notification.get('serp_domain'),
        serp_query=detail_notification.get('serp_query'),
    )

    slack_response = slack.notify(message)
    
    print(json.dumps(slack_response))

    return {'ok': True}
