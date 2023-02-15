import json
from dataclasses import asdict
from serply_config import SERPLY_CONFIG


class EventBus:

    def __init__(self, events_client: object, source: str = 'slack') -> None:
        self._events_client = events_client

    def put(self, detail_type: str, schedule: object, input: dict, headers: dict):

        event = {
            'Source': 'serply',
            'DetailType': detail_type,
            'Detail': json.dumps({
                'schedule': asdict(schedule),
                'input': input,
                'headers': headers,
            }),
            'EventBusName': SERPLY_CONFIG.EVENT_BUS_NAME,
            'TraceHeader': headers.get('X-Amzn-Trace-Id'),
        }

        return self._events_client.put_events(Entries=[event])
