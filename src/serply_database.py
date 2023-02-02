from dataclasses import asdict, dataclass, field
from serply_config import (
    datetime_string,
    default_account,
    default_domain_or_website,
    default_interval,
    default_provider,
    STAGE,
)


@dataclass
class Notification:
    SK: str = field(init=False)
    PK: str = field(init=False)
    TOKEN: str = field(init=False)
    NOTIFICATION_PK: str
    NOTIFICATION_SK: str
    query: str
    schedule_name: str
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
        self.schedule_name = f'{self.PK}#{self.SK}'


@dataclass
class Serp:
    SK: str = field(init=False)
    PK: str = field(init=False)
    NOTIFICATION_PK: str
    NOTIFICATION_SK: str
    serp_position: int
    serp_searched_results: int
    serp_domain: str
    serp_query: str
    serp_title: str
    serp_link: str
    serp_description: str
    domain_or_website: str
    query: str
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


class NotificationsDatabase:

    def __init__(self, dynamodb_resource: object) -> None:
        self._table = dynamodb_resource.Table(
            f'SerplyNotifications{STAGE.title()}'
        )

    def put(self, data):

        Item = {k: v for k, v in asdict(data).items() if v is not None}

        return self._table.put_item(Item=Item)
