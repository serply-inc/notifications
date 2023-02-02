import boto3
from serply_database import NotificationsDatabase, Notification

notifications = NotificationsDatabase(boto3.resource('dynamodb'))


def handler(event, context):

    command = event.get('detail').get('command')

    notifications.put(Notification(
        domain=command.get('domain'),
        interval=command.get('interval'),
        website=command.get('website'),
        query=command.get('query'),
    ))

    return {'ok': True}
