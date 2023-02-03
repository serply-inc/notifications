import json
from dataclasses import asdict, dataclass
from serply_config import SERPLY_CONFIG
from serply_database import Notification


@dataclass
class ScheduleResponse:
    arn: str


class NotificationScheduler:

    intervals = {
        'test': 'rate(1 minute)',
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

    def schedule(self, notification: Notification, input: dict = {}):

        response = self._scheduler_client.create_schedule(
            FlexibleTimeWindow={
                # 'MaximumWindowInMinutes': 10,
                'Mode': 'OFF', # or FLEXIBLE with MaximumWindowInMinutes
            },
            GroupName=SERPLY_CONFIG.SCHEDULE_GROUP_NAME,
            Name=notification.SCHEDULE_HASH,
            ScheduleExpression=self.intervals.get(notification.interval),
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
