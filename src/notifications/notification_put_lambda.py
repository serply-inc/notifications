import boto3
import json
from serply_database import NotificationsDatabase, notification_from_dict
from serply_scheduler import NotificationScheduler

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    notification = notification_from_dict(event.get('detail').get('notification'))
    
    notifications.put(notification)

    scheduler.schedule(
        notification=notification,
        event=event,
    )

    return {'ok': True}
