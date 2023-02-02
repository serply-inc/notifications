import boto3
from dataclasses import asdict
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

    response = serply.serp(domain=domain, query=query)

    serp = Serp(
        NOTIFICATION_PK=NOTIFICATION_PK,
        NOTIFICATION_SK=NOTIFICATION_SK,
        domain=domain,
        domain_or_website=domain_or_website,
        query=query,
        interval=interval,
        serp_position=response.position,
        serp_searched_results=response.searched_results,
        serp_domain=response.domain,
        serp_query=response.query,
        serp_title=response.title,
        serp_link=response.link,
        serp_description=response.description,
    )

    notifications.put(serp)

    return asdict(serp)
