
import datetime
from dataclasses import asdict, dataclass, field, is_dataclass
from os import getenv
from serply_config import STAGE


def default_account():
    return getenv('DEFAULT_ACCOUNT', '98a64bf66ad64b7aa23227d882d91249')


def datetime_string():
    return datetime.today().isoformat()


@dataclass
class Notification:
    SK: str = field(init=False)
    PK: str = field(init=False)
    query: str = field(init=False)
    domain: str = field(init=False)
    website: str = field(init=False)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    interval: str = 'daily'
    provider: str = 'slack'

    def __post_init__(self):
        self.PK = f'notification_{self.account}'
        self.SK = '#'.join([
            self.PK,
            f'interval_{self.interval}',
            (f'website_{self.website}', f'domain_{self.domain}')[self.website],
            f'query_{self.query}',
        ])


@dataclass
class Serp:
    SK: str = field(init=False)
    PK: str = field(init=False)
    query: str = field(init=False)
    domain: str = field(init=False)
    website: str = field(init=False)
    account: str = field(default_factory=default_account)
    created_at: str = field(default_factory=datetime_string)
    interval: str = 'daily'
    provider: str = 'slack'

    def __post_init__(self):
        self.PK = f'notification_{self.account}_serp'
        self.SK = '#'.join([
            self.PK,
            f'interval_{self.interval}',
            (f'website_{self.website}', f'domain_{self.domain}')[self.website],
            f'query_{self.query}',
        ])


class NotificationsDatabase:

    def __init__(self, dynamodb: object) -> None:
        self._dynamodb = dynamodb

    def table(self):
        return self._dynamodb.Table(f'SerplyNotifications{STAGE.title()}')

    def put(self, obj):

        if is_dataclass(obj):
            obj = asdict(obj)

        item = dict()

        for k, v in obj.items():
            if type(v) == str and len(v) > 0 or type(v) != str:
                item[k] = v

        self.table().put_item(
            Item=item,
        )
