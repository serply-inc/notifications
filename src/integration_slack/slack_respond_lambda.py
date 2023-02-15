import json
from slack_api import SlackClient
from slack_messages import ScheduledMessage
from serply_database import schedule_from_dict


slack = SlackClient()


def handler(event, context):
    
    print(json.dumps(event))

    # detail_type = event.get('detail-type')
    detail_input = event.get('detail').get('input')
    schedule = schedule_from_dict(event.get('detail').get('schedule'))

    message = ScheduledMessage(
        channel=detail_input.get('channel_id'),
        user_id=detail_input.get('user_id'),
        command=schedule.command,
        interval=schedule.interval,
        type=schedule.type,
        domain=schedule.domain,
        domain_or_website=schedule.domain_or_website,
        query=schedule.query,
        website=schedule.website,
    )

    slack.respond(
        response_url=detail_input.get('response_url'),
        message=message,
    )

    return {'ok': True}
