from dataclasses import dataclass, field
from utils import default_account, datetime_string


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


class NotificationProvider:

    def __init__(self, serply: object, repository: object, secrets: object) -> None:
        self._repository = repository
        self._secrets = secrets
        self._serply = serply

    def configure(self, event: dict, context: dict):
        print('configure is not implemented')
        print(input)

    def notify(self, event: dict, context: dict):
        print('notify is not implemented')
        print(input)

    def serp(self, event: dict, context: dict):
        print('serp is not implemented')
        print(input)
