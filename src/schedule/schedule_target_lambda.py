import boto3
import json
from dataclasses import asdict
from serply_api import SerplyClient
from serply_config import SERPLY_CONFIG
from serply_database import NotificationsDatabase, SerpNotification, schedule_from_dict
from serply_events import EventBus

event_bus = EventBus(boto3.client('events'))
notifications = NotificationsDatabase(boto3.resource('dynamodb'))
serply = SerplyClient(SERPLY_CONFIG.SERPLY_API_KEY)


def handler(event, context):

    print(json.dumps(event))

    detail_headers = event.get('detail').get('headers')
    detail_schedule = event.get('detail').get('schedule')
    detail_input = event.get('detail').get('input')

    schedule = schedule_from_dict(detail_schedule)

    if schedule.type not in [SERPLY_CONFIG.SCHEDULE_TYPE_SERP]:
        raise Exception(f'Invalid schedule type: {schedule.type}')

    if schedule.type == SERPLY_CONFIG.SCHEDULE_TYPE_SERP:

        response = serply.serp(
            domain=schedule.domain,
            website=schedule.website,
            query=schedule.query,
            mock=schedule.interval == 'mock',
        )

        notification = SerpNotification(
            command=schedule.command,
            domain=schedule.domain,
            domain_or_website=schedule.domain_or_website,
            query=schedule.query,
            interval=schedule.interval,
            serp_position=response.position,
            serp_searched_results=response.searched_results,
        )

    notifications.save(notification)

    notification_input = asdict(notification)

    event_bus.put(
        source=schedule.source,
        detail_type=SERPLY_CONFIG.EVENT_SCHEDULE_NOTIFY,
        schedule=schedule,
        input={
            **detail_input,
            **notification_input,
        },
        headers=detail_headers,
    )

    return {'ok': True}
