import json
from dataclasses import asdict, dataclass
from serply_config import STAGE, SERPLY_TIMEZONE
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
        self._event_bus_name = f'NotificationsEventBus{STAGE.title()}'
        self._schedule_group = f'NotificationScheduleGroup{STAGE.title()}'

    def schedule(self, notification: Notification, target_arn: str, role_arn: str):

        flexible_time_window = {
            'MaximumWindowInMinutes': 10,
            'Mode': 'FLEXIBLE',
        }

        if notification.interval == 'test':
            flexible_time_window = {
                'Mode': 'OFF',
            }

        response = self._scheduler_client.create_schedule(
            FlexibleTimeWindow=flexible_time_window,
            GroupName=self._schedule_group,
            Name=notification.SCHEDULE_HASH,
            ScheduleExpression=self.intervals.get(notification.interval),
            ScheduleExpressionTimezone=SERPLY_TIMEZONE,
            State='ENABLED',
            Target={
                'Arn': target_arn,
                'Input': json.dumps(asdict(notification)),
                'RetryPolicy': {
                    'MaximumRetryAttempts': self.max_retry_attempts.get(notification.interval),
                },
                'RoleArn': role_arn,
            }
        )

        return ScheduleResponse(arn=response.get('ScheduleArn'))
