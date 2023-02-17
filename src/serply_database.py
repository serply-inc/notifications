from hashlib import blake2b
from dataclasses import asdict, dataclass, field
from serply_config import (
    datetime_string,
    default_account,
    default_schedule_type,
    default_domain_or_website,
    default_interval,
    default_source,
    SERPLY_CONFIG,
)


@dataclass
class Schedule:
    PK: str = field(init=False)
    SK: str = field(init=False)
    hash: str = field(init=False)
    collection: str = field(init=False)
    command: str
    query: str
    type: str = field(default_factory=default_schedule_type)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    domain_or_website: str = field(default_factory=default_domain_or_website)
    interval: str = field(default_factory=default_interval)
    source: str = field(default_factory=default_source)
    domain: str = None
    enabled: bool = True
    website: str = None
    num: int = 100

    def __post_init__(self):
        SCHEDULE_KEY = 'schedule_' + schedule_key(self)
        self.PK = SCHEDULE_KEY
        self.SK = SCHEDULE_KEY
        self.domain_or_website = domain_or_website(self.domain)
        self.hash = schedule_hash(SCHEDULE_KEY)
        self.collection = f'{self.account}#schedules'


@dataclass
class SerpNotification:
    PK: str = field(init=False)
    SK: str = field(init=False)
    hash: str = field(init=False)
    collection: str = field(init=False)
    command: str
    serp_position: int
    serp_searched_results: int
    domain_or_website: str
    query: str
    type: str = 'serp'
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    interval: str = field(default_factory=default_interval)
    source: str = field(default_factory=default_source)
    domain: str = None
    website: str = None
    num: int = 100

    def __post_init__(self):
        SCHEDULE_KEY = 'schedule_' + schedule_key(self)
        NOTIFICATION_KEY = 'notification_' + \
            schedule_key(self) + f'#{self.created_at}'
        self.PK = SCHEDULE_KEY
        self.SK = NOTIFICATION_KEY
        self.domain_or_website = domain_or_website(self.domain)
        self.hash = schedule_hash(SCHEDULE_KEY)
        self.collection = f'{self.account}#serp'


class NotificationsDatabase:

    def __init__(self, dynamodb_resource: object) -> None:
        self._table = dynamodb_resource.Table(
            SERPLY_CONFIG.NOTIFICATION_TABLE_NAME
        )

    def save(self, data):
        # Filter values that are None
        item = {k: v for k, v in asdict(data).items() if v is not None}
        return self._table.put_item(Item=item)

    def schedules(self) -> list[Schedule]:
        response = self._table.query(
            IndexName='CollectionIndex',
            KeyConditions={
                'collection': {
                    'AttributeValueList': [f'{default_account()}#schedules'],
                    'ComparisonOperator': 'EQ',
                },
                'SK': {
                    'AttributeValueList': ['schedule_'],
                    'ComparisonOperator': 'BEGINS_WITH',
                }
            },
        )

        return map(schedule_from_dict, response.get('Items') or [])


def domain_or_website(domain: str = None):
    return 'domain' if domain else 'website'


def schedule_key(object):
    attributes = [
        object.account,
        object.type,
        domain_or_website(object.domain),
        object.domain if object.domain else object.website,
        object.query,
    ]

    if object.interval in SERPLY_CONFIG.ONE_TIME_INTERVALS:
        attributes.append(object.interval)

    attributes = list(filter(lambda a: a is not None, attributes))

    return '#'.join(attributes)


def schedule_hash(SCHEDULE_KEY: str):
    # 32 bytes will result in a 64 character hash
    return blake2b(bytes(SCHEDULE_KEY, 'utf-8'), digest_size=32).hexdigest()


def schedule_from_dict(data: dict):
    return Schedule(
        interval=data.get('interval'),
        query=data.get('query'),
        command=data.get('command'),
        enabled=data.get('enabled'),
        domain=data.get('domain'),
        type=data.get('type'),
        website=data.get('website'),
        # num=data.get('num'), # @todo parse number
    )
