from hashlib import blake2b
from dataclasses import asdict, dataclass, field
from serply_config import (
    datetime_string,
    default_account,
    default_notification_type,
    default_domain_or_website,
    default_interval,
    default_provider,
    SERPLY_CONFIG,
)


def schedule_hash(obj: str):
    return blake2b(bytes(f'{obj.NOTIFICATION_PK}#{obj.NOTIFICATION_SK}', 'utf-8'), digest_size=32).hexdigest()


@dataclass
class Notification:
    SK: str = field(init=False)
    PK: str = field(init=False)
    SCHEDULE_HASH: str = field(init=False)
    NOTIFICATION_PK: str = field(init=False)
    NOTIFICATION_SK: str = field(init=False)
    query: str
    type: str = field(default_factory=default_notification_type)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    domain_or_website: str = field(default_factory=default_domain_or_website)
    interval: str = field(default_factory=default_interval)
    provider: str = field(default_factory=default_provider)
    domain: str = None
    website: str = None
    num: int = 100

    def __post_init__(self):
        self.domain_or_website = 'domain' if self.domain else 'website'
        self.PK = f'notification_{self.account}'
        self.SK = '#'.join([
            f'domain_{self.domain}' if self.domain else f'website_{self.website}',
            f'query_{self.query}',
        ])
        self.NOTIFICATION_PK = self.PK
        self.NOTIFICATION_SK = self.SK
        self.SCHEDULE_HASH = schedule_hash(self)


@dataclass
class SerpNotification:
    SK: str = field(init=False)
    PK: str = field(init=False)
    SCHEDULE_HASH: str = field(init=False)
    NOTIFICATION_PK: str
    NOTIFICATION_SK: str
    serp_position: int
    serp_searched_results: int
    serp_domain: str
    serp_query: str
    domain_or_website: str
    query: str
    type: str = 'serp'
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    interval: str = field(default_factory=default_interval)
    provider: str = field(default_factory=default_provider)
    domain: str = None
    website: str = None
    num: int = 100

    def __post_init__(self):
        self.PK = '#'.join([
            self.NOTIFICATION_PK,
            self.NOTIFICATION_SK,
        ])
        self.SK = f'serp_{self.created_at}'
        self.SCHEDULE_HASH = schedule_hash(self)


class NotificationsDatabase:

    def __init__(self, dynamodb_resource: object) -> None:
        self._table = dynamodb_resource.Table(
            SERPLY_CONFIG.NOTIFICATION_TABLE_NAME
        )

    def put(self, data):
        # Filter values that are None
        item = {k: v for k, v in asdict(data).items() if v is not None}
        return self._table.put_item(Item=item)
