
from datetime import datetime
from dataclasses import asdict, dataclass, field
from os import getenv
from serply_config import STAGE


def default_account():
    return getenv('DEFAULT_ACCOUNT', '98a64bf66ad64b7aa23227d882d91249')


def datetime_string():
    return datetime.today().isoformat()


def default_domain_or_website():
    return 'domain'


def default_interval():
    return 'daily'


def default_provider():
    return 'slack'


@dataclass
class Notification:
    SK: str = field(init=False)
    PK: str = field(init=False)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    domain_or_website: str = field(default_factory=default_domain_or_website)
    interval: str = field(default_factory=default_interval)
    provider: str = field(default_factory=default_provider)
    query: str = ''
    domain: str = ''
    website: str = ''

    def __post_init__(self):
        self.PK = f'notification_{self.account}'
        self.SK = '#'.join([
            self.PK,
            f'interval_{self.interval}',
            f'domain_{self.domain}' if self.domain else f'website_{self.website}',
            f'query_{self.query}',
        ])
        self.domain_or_website = 'domain' if self.domain else self.website


@dataclass
class Serp:
    SK: str = field(init=False)
    PK: str = field(init=False)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    domain_or_website: str = field(default_factory=default_domain_or_website)
    interval: str = field(default_factory=default_interval)
    provider: str = field(default_factory=default_provider)
    query: str = ''
    domain: str = ''
    website: str = ''

    def __post_init__(self):
        self.PK = f'notification_{self.account}_serp'
        self.SK = '#'.join([
            self.PK,
            datetime_string(),
            f'interval_{self.interval}',
            f'domain_{self.domain}' if self.domain else f'website_{self.website}',
            f'query_{self.query}',
        ])
        self.domain_or_website = 'domain' if self.domain else 'website'


class NotificationsDatabase:

    def __init__(self, dynamodb_resource: object) -> None:
        self._table = dynamodb_resource.Table(
            f'SerplyNotifications{STAGE.title()}'
        )

    def put(self, data):

        Item = {k: v for k, v in asdict(data).items() if v is not None}

        return self._table.put_item(Item=Item)
