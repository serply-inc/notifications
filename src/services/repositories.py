from dataclasses import asdict, is_dataclass
from providers.notification_provider import Notification


class DynamoDBNotificationsRepository:

    def __init__(self, stage_name: str, dynamodb: object) -> None:
        self._stage_name = stage_name
        self._dynamodb = dynamodb

    def table(self):
        return self._dynamodb.Table(f'SerplyNotifications-{self._stage_name}')

    def save_notification(self, notification=Notification):
        print(notification)
        self.put_item(notification)

    def put_item(self, obj):

        if is_dataclass(obj):
            obj = asdict(obj)

        item = dict()

        for k, v in obj.items():
            if type(v) == str and len(v) > 0 or type(v) != str:
                item[k] = v

        self.table().put_item(
            Item=item,
        )
