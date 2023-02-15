import boto3
import json
from serply_api import SerplyClient
from serply_config import SERPLY_CONFIG
from serply_database import NotificationsDatabase, SerpNotification, schedule_from_dict
from serply_events import EventBus

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
notification_event_bus = EventBus(boto3.client('events'))
serply = SerplyClient(SERPLY_CONFIG.SERPLY_API_KEY)


def handler(event, context):

    print(json.dumps(event))

    detail_input = event.get('detail').get('input')
    detail_headers = event.get('detail').get('headers')

    schedule = schedule_from_dict(event.get('detail').get('schedule'))

    response = serply.serp(
        domain=schedule.domain,
        website=schedule.website,
        query=schedule.query,
        mock=schedule.interval == 'mock',
    )

    serp_notification = SerpNotification(
        domain=schedule.domain,
        domain_or_website=schedule.domain_or_website,
        query=schedule.query,
        interval=schedule.interval,
        serp_position=response.position,
        serp_searched_results=response.searched_results,
        serp_domain=response.domain,
        serp_query=response.query,
    )

    notifications.put(serp_notification)

    notification_event_bus.put(
        detail_type=f'{schedule.type}.notify',
        schedule=serp_notification,
        input=detail_input,
        headers=detail_headers,
    )

    return {'ok': True}
