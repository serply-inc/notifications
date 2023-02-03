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
        self._event_bus_name = SERPLY_CONFIG.EVENT_BUS_NAME
        self._schedule_group_name = SERPLY_CONFIG.SCHEDULE_GROUP_NAME

    def schedule(self, notification: Notification, input: dict = {}, headers: dict = {}):

        response = self._scheduler_client.create_schedule(
            FlexibleTimeWindow={
                'MaximumWindowInMinutes': 10,
                'Mode': 'OFF' if notification.interval == 'test' else 'FLEXIBLE',
            },
            GroupName=self._schedule_group_name,
            Name=notification.SCHEDULE_HASH,
            ScheduleExpression=self.intervals.get(notification.interval),
            ScheduleExpressionTimezone=SERPLY_CONFIG.SERPLY_TIMEZONE,
            State='ENABLED',
            Target={
                'Arn': SERPLY_CONFIG.SCHEDULE_TARGET_ARN,
                'RoleArn': SERPLY_CONFIG.SCHEDULE_ROLE_ARN,
                'Input': json.dumps({
                    'notification': asdict(notification),
                    'input': input,
                    'headers': headers,
                }),
                'RetryPolicy': {
                    'MaximumRetryAttempts': self.max_retry_attempts.get(notification.interval),
                },
            }
        )

        return ScheduleResponse(arn=response.get('ScheduleArn'))
