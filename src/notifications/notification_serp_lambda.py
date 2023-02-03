import boto3
import json
from serply_api import SerplyClient
from serply_config import SERPLY_CONFIG
from serply_database import NotificationsDatabase, Serp

notifications = NotificationsDatabase(boto3.resource('dynamodb'))
serply = SerplyClient(SERPLY_CONFIG.SERPLY_API_KEY)

events = boto3.client('events')


def handler(event, context):

    print(json.dumps(event))

    input = event.get('input')

    mock = input.get('interval') == 'test'

    response = serply.serp(
        domain=input.get('domain'),
        website=input.get('website'),
        query=input.get('query'),
        mock=mock,
    )

    serp = Serp(
        NOTIFICATION_PK=input.get('NOTIFICATION_PK'),
        NOTIFICATION_SK=input.get('NOTIFICATION_SK'),
        domain=input.get('domain'),
        domain_or_website=input.get('domain_or_website'),
        query=input.get('query'),
        interval=input.get('interval'),
        serp_position=response.position,
        serp_searched_results=response.searched_results,
        serp_domain=response.domain,
        serp_query=response.query,
        serp_title=response.title,
        serp_link=response.link,
        serp_description=response.description,
    )

    notifications.put(serp)

    events.trigger(
        notification=event.get('notification'),
        input=event.get('input'),
        headers=event.get('headers'),
    )

    return {'ok': True}
