import json
from dataclasses import asdict
from serply_config import SERPLY_CONFIG


class NotificationEvents:

    def __init__(self, events_client: object) -> None:
        self._events_client = events_client
        self._event_bus_name = SERPLY_CONFIG.EVENT_BUS_NAME

    def trigger(self, notification: object, input: dict, headers: dict):

        event = {
            'Source': 'serply',
            'DetailType': notification.type,
            'Detail': json.dumps({
                'notification': asdict(notification),
                'input': input,
                'headers': headers,
            }),
            'EventBusName': self._event_bus_name,
            'TraceHeader': headers.get('X-Amzn-Trace-Id')
        }

        return self._events_client.put_events(Entries=[event])
