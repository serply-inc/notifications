import json
from dataclasses import asdict, is_dataclass
from serply_config import SERPLY_CONFIG


class EventBus:

    def __init__(self, events_client: object) -> None:
        self._events_client = events_client

    def put(self, source: str, detail_type: str, schedule: object, input: object, headers: dict):

        event = {
            'Source': source,
            'DetailType': detail_type,
            'Detail': json.dumps({
                'schedule': asdict(schedule) if is_dataclass(schedule) else schedule,
                'input': asdict(input) if is_dataclass(input) else input,
                'headers': headers,
            }),
            'EventBusName': SERPLY_CONFIG.EVENT_BUS_NAME,
            'TraceHeader': headers.get('X-Amzn-Trace-Id'),
        }

        return self._events_client.put_events(Entries=[event])
