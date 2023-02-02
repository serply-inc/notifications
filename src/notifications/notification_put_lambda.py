import boto3
from os import getenv
from serply_database import NotificationsDatabase, Notification

DEFAULT_ACCOUNT = getenv('DEFAULT_ACCOUNT')


notifications = NotificationsDatabase(boto3.resource('dynamodb'))


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
