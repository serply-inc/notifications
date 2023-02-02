import boto3
from os import getenv
# from serply_api import SerplyClient
from serply_database import NotificationsDatabase, Serp

DEFAULT_ACCOUNT = getenv('DEFAULT_ACCOUNT')


# serply = SerplyClient()
notifications = NotificationsDatabase(boto3.resource('dynamodb'))


def handler(event, context):

    # command = event.get('detail').get('command')

    # notifications.put(Serp(
    #     account=DEFAULT_ACCOUNT,
    #     provider=command.get('provider'),
    #     interval=command.get('interval'),
    #     website=command.get('website'),
    #     domain=command.get('domain'),
    #     query=command.get('query'),
    # ))

    notifications.put(Serp(
        account=DEFAULT_ACCOUNT,
        domain='hashnode.com',
        query='developer+blog+platform',
        serp_position=45,
        serp_searched_results=67,
        serp_domain='.hashnode.com',
        serp_query='q="developer+blog+platform&num=100"',
    ))

    return {'ok': True}
