import boto3
from os import getenv
from serply_api import SerplyClient
from serply_database import NotificationsDatabase, Serp


notifications = NotificationsDatabase(boto3.resource('dynamodb'))
serply = SerplyClient(getenv('SERPLY_API_KEY'))


def handler(event, context):

    NOTIFICATION_PK = 'notification_98a64bf66ad64b7aa23227d882d91249'
    NOTIFICATION_SK = 'domain_google.com#query_google+search+api'
    domain = 'hashnode.com'
    domain_or_website = 'domain'
    query = 'developer+blog'
    interval = 'test'

    serp = serply.serp(domain=domain, query=query)

    notifications.put(Serp(
        NOTIFICATION_PK=NOTIFICATION_PK,
        NOTIFICATION_SK=NOTIFICATION_SK,
        domain=domain,
        domain_or_website=domain_or_website,
        query=query,
        interval=interval,
        serp_position=serp.position,
        serp_searched_results=serp.searched_results,
        serp_domain=serp.domain,
        serp_query=serp.query,
    ))

    return {'ok': True}
