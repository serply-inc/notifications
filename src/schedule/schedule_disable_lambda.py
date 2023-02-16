import boto3
import json
from serply_database import schedule_from_dict
from serply_scheduler import NotificationScheduler

scheduler = NotificationScheduler(boto3.client('scheduler'))


def handler(event, context):

    print(json.dumps(event))

    schedule = schedule_from_dict(event.get('detail').get('schedule'))
    
    scheduler.delete_schedule(schedule)
    
    return {'ok': True}
