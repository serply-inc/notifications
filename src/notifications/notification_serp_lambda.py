import boto3
from os import getenv
from serply_database import NotificationsDatabase, Notification

notifications = NotificationsDatabase(boto3.resource('dynamodb'))

DEFAULT_ACCOUNT = getenv('DEFAULT_ACCOUNT')


def handler(event, context):

    # command = event.get('detail').get('command')

    # 1. Gather params
    # 2. Check if there is a scheduler for a given inter

    # notification = Notification(
    #     account=DEFAULT_ACCOUNT,
    #     provider=command.get('provider', 'slack'),
    #     interval=command.get('interval', 'daily'),
    #     website=command.get('website',''),
    #     domain=command.get('domain',''),
    #     query=command.get('query',''),
    # )

    # notifications.put(notification)

    return {'ok', True}
