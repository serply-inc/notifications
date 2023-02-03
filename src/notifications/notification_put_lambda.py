import boto3
import json
from serply_database import NotificationsDatabase, Notification
from serply_scheduler import NotificationScheduler

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    detail_type = event.get('detail-type')
    detail_notification = event.get('detail').get('notification')

    notification = Notification(
        type=detail_type,
        domain=detail_notification.get('domain'),
        interval=detail_notification.get('interval'),
        website=detail_notification.get('website'),
        query=detail_notification.get('query'),
    )

    notifications.put(notification)

    scheduler.schedule(
        notification=notification,
        input=event
    )

    return {'ok': True}
