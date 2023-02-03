import json
import boto3
from dataclasses import asdict
from os import getenv
from serply_api import SerplyClient
from serply_database import NotificationsDatabase, Serp

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
serply = SerplyClient(getenv('SERPLY_API_KEY'))


def handler(schedule_event, context):

    print(json.dumps(schedule_event))

    NOTIFICATION_PK = schedule_event.get('NOTIFICATION_PK')
    NOTIFICATION_SK = schedule_event.get('NOTIFICATION_SK')
    domain = schedule_event.get('domain')
    website = schedule_event.get('website')
    domain_or_website = schedule_event.get('domain_or_website')
    query = schedule_event.get('query')
    interval = schedule_event.get('interval')

    if interval == 'test':
        response = serply.serp(domain=domain, website=website, query=query)
    else:
        response = serply.serpMock(domain=domain, website=website, query=query)

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
