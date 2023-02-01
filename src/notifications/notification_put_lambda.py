import boto3
from os import getenv
from serply_database import NotificationsDatabase, Notification

notifications = NotificationsDatabase(boto3.resource('dynamodb'))

DEFAULT_ACCOUNT = getenv('DEFAULT_ACCOUNT')

def handler(event, context):

    command = event.get('detail').get('command')

    # 1. Gather params
    # 2. Check if there is a scheduler for a given inter
    
    notifications.put(Notification(
        account=
    ))

    return {'ok', True}
