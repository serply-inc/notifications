import boto3
import json
from serply_database import NotificationsDatabase, Notification
from serply_scheduler import NotificationScheduler

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    input = event.get('detail').get('input')
    headers = event.get('detail').get('headers')

    notification = Notification(
        type=input.get('detail-type'),
        domain=input.get('domain'),
        interval=input.get('interval'),
        website=input.get('website'),
        query=input.get('query'),
    )

    notifications.put(notification)

    scheduler.schedule(
        notification=notification,
        input=input,
        headers=headers,
    )

    return {'ok': True}
