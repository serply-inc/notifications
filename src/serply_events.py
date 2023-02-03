import json
from dataclasses import asdict
from serply_config import SERPLY_CONFIG


class NotificationEventBus:

    def __init__(self, events_client: object) -> None:
        self._events_client = events_client

    def put(self, detail_type: str, notification: object, input: dict, headers: dict):

        print(f'detail_type: {detail_type}')

        event = {
            'Source': 'serply',
            'DetailType': detail_type,
            'Detail': json.dumps({
                'notification': asdict(notification),
                'input': input,
                'headers': headers,
            }),
            'EventBusName': SERPLY_CONFIG.EVENT_BUS_NAME,
            'TraceHeader': headers.get('X-Amzn-Trace-Id'),
        }

        return self._events_client.put_events(Entries=[event])
