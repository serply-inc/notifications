import json
from datetime import datetime
from dataclasses import dataclass
from serply_config import SERPLY_CONFIG
from serply_database import Notification


@dataclass
class ScheduleResponse:
    arn: str = None
    name: str = None


class NotificationScheduler:

    intervals = {
        'daily': 'rate(1 day)',
        'weekly': 'rate(1 week)',
        'monthly': 'rate(1 month)',
    }

    max_retry_attempts = {
        'test': 0,
        'daily': 1,
        'weekly': 2,
        'monthly': 3,
    }

    def __init__(self, scheduler_client: object) -> None:
        self._scheduler_client = scheduler_client

    def create_schedule(self, notification: Notification, input: dict = {}):

        schedule_expression = self.intervals.get(notification.interval)

        # If this is a test, set a one-time schedule expression at(yyyy-mm-ddThh:mm:ss).
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client.create_schedule
        # https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html#one-time
        if 'test' in notification.interval:

            schedule_expression = f'at({datetime.today().isoformat(timespec="seconds")})'

        response = self._scheduler_client.create_schedule(
            FlexibleTimeWindow={
                # 'MaximumWindowInMinutes': 10,
                'Mode': 'OFF',  # or FLEXIBLE with MaximumWindowInMinutes
            },
            GroupName=SERPLY_CONFIG.SCHEDULE_GROUP_NAME,
            Name=notification.SCHEDULE_HASH,
            ScheduleExpression=schedule_expression,
            ScheduleExpressionTimezone=SERPLY_CONFIG.SERPLY_TIMEZONE,
            State='ENABLED',
            Target={
                'Arn': SERPLY_CONFIG.SCHEDULE_TARGET_ARN,
                'RoleArn': SERPLY_CONFIG.SCHEDULE_ROLE_ARN,
                'Input': json.dumps(input),
                'RetryPolicy': {
                    'MaximumRetryAttempts': self.max_retry_attempts.get(notification.interval),
                },
            }
        )

        return ScheduleResponse(arn=response.get('ScheduleArn'))

    def delete_schedule(self, notification: Notification):

        name = notification.SCHEDULE_HASH

        try:

            self._scheduler_client.delete_schedule(
                GroupName=SERPLY_CONFIG.SCHEDULE_GROUP_NAME,
                ClientToken=name,
                Name=name
            )

            return ScheduleResponse(name=name)

        except:

            return ScheduleResponse(name=name)

    def get_schedule(self, notification: Notification):

        name = notification.SCHEDULE_HASH

        try:

            response = self._scheduler_client.get_schedule(
                GroupName=SERPLY_CONFIG.SCHEDULE_GROUP_NAME,
                Name=notification.SCHEDULE_HASH,
            )

            return ScheduleResponse(name=name, arn=response.get('Arn'))

        except:

            return ScheduleResponse(name=name)

    def schedule(self, notification: Notification, input: dict = {}):

        self.delete_schedule(notification=notification)

        schedule = self.create_schedule(
            notification=notification,
            input=input,
        )

        return schedule
