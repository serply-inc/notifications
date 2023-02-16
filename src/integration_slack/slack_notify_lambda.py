import boto3
import json
from serply_config import SERPLY_CONFIG
from slack_api import SlackClient
from slack_messages import SerpNotificationMessage
from serply_database import schedule_from_dict
from serply_scheduler import NotificationScheduler


slack = SlackClient(SERPLY_CONFIG.SLACK_BOT_TOKEN)
scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    detail_schedule = event.get('detail').get('schedule')
    detail_input = event.get('detail').get('input')

    schedule = schedule_from_dict(detail_schedule)

    message = SerpNotificationMessage(
        channel=detail_input.get('channel_id'),
        serp_position=detail_schedule.get('serp_position'),
        serp_searched_results=detail_schedule.get('serp_searched_results'),
        command=schedule.command,
        domain=schedule.domain,
        domain_or_website=schedule.domain_or_website,
        interval=schedule.interval,
        query=schedule.query,
        website=schedule.website,
    )

    slack.notify(message)

    if schedule.interval in SERPLY_CONFIG.ONE_TIME_INTERVALS:

        scheduler.delete_schedule(schedule)

    return {'ok': True}
