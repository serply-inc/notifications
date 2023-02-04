import boto3
import json
from serply_api import SerplyClient
from serply_config import SERPLY_CONFIG
from serply_database import NotificationsDatabase, SerpNotification, notification_from_dict
from serply_events import NotificationEventBus

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
notification_event_bus = NotificationEventBus(boto3.client('events'))
serply = SerplyClient(SERPLY_CONFIG.SERPLY_API_KEY)


def handler(event, context):

    print(json.dumps(event))

    detail_input = event.get('detail').get('input')
    detail_headers = event.get('detail').get('headers')

    notification = notification_from_dict(event.get('detail').get('notification'))

    response = serply.serp(
        domain=notification.domain,
        website=notification.website,
        query=notification.query,
        mock=notification.interval == 'mock',
    )

    serp_notification = SerpNotification(
        NOTIFICATION_PK=notification.PK,
        NOTIFICATION_SK=notification.SK,
        domain=notification.domain,
        domain_or_website=notification.domain_or_website,
        query=notification.query,
        interval=notification.interval,
        serp_position=response.position,
        serp_searched_results=response.searched_results,
        serp_domain=response.domain,
        serp_query=response.query,
    )

    notifications.put(serp_notification)

    notification_event_bus.put(
        detail_type=f'{notification.type}.notify',
        notification=serp_notification,
        input=detail_input,
        headers=detail_headers,
    )

    return {'ok': True}
