from pydash import objects
from slack_api import SlackClient, SlackCommand
from slack_messages import ScheduleMessage
from serply_config import SERPLY_CONFIG
from serply_database import schedule_from_dict


slack = SlackClient()


def handler(event, context):

    detail_type = event.get('detail-type')
    detail_input = event.get('detail').get('input')
    detail_schedule = event.get('detail').get('schedule')
    
    
    if detail_type == SERPLY_CONFIG.EVENT_SCHEDULE_SAVE:
        schedule = schedule_from_dict(detail_schedule)
        message = ScheduleMessage(
            channel=detail_input.get('channel_id'),
            user_id=detail_input.get('user_id'),
            command=schedule.command,
            interval=schedule.interval,
            type=schedule.type,
            domain=schedule.domain,
            domain_or_website=schedule.domain_or_website,
            query=schedule.query,
            website=schedule.website,
            enabled=True,
            replace_original=False,
        )
    elif detail_type == SERPLY_CONFIG.EVENT_SCHEDULE_DISABLE:
        schedule = SlackCommand(
            command=objects.get(detail_input, 'actions[0].value'),
        )
        message = ScheduleMessage(
            user_id=detail_input.get('user').get('id'),
            command=schedule.command,
            interval=schedule.interval,
            type=schedule.type,
            domain=schedule.domain,
            domain_or_website=schedule.domain_or_website,
            query=schedule.query,
            website=schedule.website,
            enabled=False,
            replace_original=True,
        )
    elif detail_type == SERPLY_CONFIG.EVENT_SCHEDULE_ENABLE:
        schedule = SlackCommand(
            command=objects.get(detail_input, 'actions[0].value'),
        )
        message = ScheduleMessage(
            user_id=detail_input.get('user').get('id'),
            command=schedule.command,
            interval=schedule.interval,
            type=schedule.type,
            domain=schedule.domain,
            domain_or_website=schedule.domain_or_website,
            query=schedule.query,
            website=schedule.website,
            enabled=True,
            replace_original=True,
        )

    print(message)

    response = slack.respond(
        response_url=detail_input.get('response_url'),
        message=message,
    )

    print(response)

    return {'ok': True}
