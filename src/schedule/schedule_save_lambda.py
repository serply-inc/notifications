import boto3
import json
from serply_database import NotificationsDatabase, schedule_from_dict
from serply_scheduler import NotificationScheduler

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    schedule = schedule_from_dict(event.get('detail').get('schedule'))
    
    notifications.save(schedule)

    scheduler.save_schedule(
        schedule=schedule,
        event=event,
    )
    
    return {'ok': True}
