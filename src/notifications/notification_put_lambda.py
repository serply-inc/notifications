import boto3
from os import getenv
from dataclasses import asdict
from serply_database import NotificationsDatabase, Notification
from serply_scheduler import NotificationScheduler

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    command = event.get('detail').get('command')

    notification = Notification(
        domain=command.get('domain'),
        interval=command.get('interval'),
        website=command.get('website'),
        query=command.get('query'),
    )

    notifications.put(notification)

    schedule = scheduler.schedule(
        notification,
        getenv('SCHEDULE_TARGET_ARN'),
        getenv('SCHEDULE_ROLE_ARN'),
    )

    print(schedule.arn)

    return asdict(notification)
