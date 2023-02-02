import boto3
from os import getenv
from serply_database import NotificationsDatabase, Notification

notifications = NotificationsDatabase(boto3.resource('dynamodb'))

DEFAULT_ACCOUNT = getenv('DEFAULT_ACCOUNT')


def handler(event, context):

    command = event.get('detail').get('command')

    notifications.put(Notification(
        account=DEFAULT_ACCOUNT,
        provider=command.get('provider'),
        interval=command.get('interval'),
        website=command.get('website'),
        domain=command.get('domain'),
        query=command.get('query'),
    ))

    return {'ok': True}
