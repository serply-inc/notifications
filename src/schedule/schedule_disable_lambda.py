import boto3
import json
from serply_database import NotificationsDatabase, schedule_from_dict
from serply_scheduler import NotificationScheduler


notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    detail_schedule = event.get('detail').get('schedule')

    schedule = schedule_from_dict(detail_schedule)

    scheduler.delete_schedule(schedule)

    schedule.enabled = False

    notifications.save(schedule)

    return event
