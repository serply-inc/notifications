from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from os import getenv, path


STAGE = getenv('STAGE', 'dev')


load_dotenv(f'.env.{STAGE}')


STACK_NAME = getenv('STACK_NAME', 'Serply')
STAGE_SUFFIX = STAGE.title()
STACK_NAME_FULL = f'{STACK_NAME}Stack{STAGE_SUFFIX}'
SRC_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.dirname(SRC_DIR)


@dataclass
class SerplyConfig:
    AWS_PROFILE: str
    DEFAULT_ACCOUNT: str
    EVENT_BUS_NAME: str
    LAYER_DIR: str
    NOTIFICATION_TABLE_NAME: str
    NOTIFICATIONS_DIR: str
    ONE_TIME_INTERVALS: list[str]
    ROOT_DIR: str
    SCHEDULE_GROUP_NAME: str
    SCHEDULE_ROLE_ARN: str
    SCHEDULE_TARGET_ARN: str
    SCHEDULE_TYPE_SERP: str
    SECRET_KEYS: list[str]
    SERPLY_API_KEY: str
    SERPLY_TIMEZONE: str
    SLACK_BOT_TOKEN: str
    SLACK_DIR: str
    SRC_DIR: str
    STACK_NAME: str
    STACK_NAME_FULL: str
    STAGE: str
    STAGE_SUFFIX: str
    TYPE_NAME_MAP: dict
    EVENT_SOURCE_SLACK: str
    EVENT_SCHEDULE_SAVE: str
    EVENT_SCHEDULE_NOTIFY: str
    EVENT_SCHEDULE_DISABLE: str
    EVENT_SCHEDULE_LIST: str


SERPLY_CONFIG = SerplyConfig(
    AWS_PROFILE=getenv('AWS_PROFILE', 'default'),
    DEFAULT_ACCOUNT=getenv('ACCOUNT', '98a64bf66ad64b7aa23227d882d91249'),
    EVENT_BUS_NAME=f'{STACK_NAME}EventBus{STAGE_SUFFIX}',
    LAYER_DIR=f'{SRC_DIR}/layer',
    NOTIFICATIONS_DIR=f'{SRC_DIR}/schedule',
    NOTIFICATION_TABLE_NAME=f'{STACK_NAME}Notifications{STAGE_SUFFIX}',
    ONE_TIME_INTERVALS=['once', 'mock'],
    ROOT_DIR=ROOT_DIR,
    SCHEDULE_GROUP_NAME=f'{STACK_NAME}ScheduleGroup{STAGE_SUFFIX}',
    SCHEDULE_ROLE_ARN=getenv('SCHEDULE_ROLE_ARN'),
    SCHEDULE_TARGET_ARN=getenv('SCHEDULE_TARGET_ARN'),
    SCHEDULE_TYPE_SERP='serp',
    SECRET_KEYS=[
        'ACCOUNT',
        'SLACK_BOT_TOKEN',
        'SLACK_SIGNING_SECRET',
        'SERPLY_API_KEY',
    ],
    SERPLY_API_KEY=getenv('SERPLY_API_KEY'),
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    SERPLY_TIMEZONE=getenv('SERPLY_TIMEZONE', 'America/Chicago'),
    SRC_DIR=SRC_DIR,
    SLACK_BOT_TOKEN=getenv('SLACK_BOT_TOKEN'),
    SLACK_DIR=f'{SRC_DIR}/slack',
    STACK_NAME=STACK_NAME,
    STACK_NAME_FULL=STACK_NAME_FULL,
    STAGE=STAGE,
    STAGE_SUFFIX=STAGE_SUFFIX,
    TYPE_NAME_MAP={'serp': 'SERP'},
    EVENT_SOURCE_SLACK='slack',
    EVENT_SCHEDULE_SAVE='schedule.save',
    EVENT_SCHEDULE_DISABLE='schedule.disable',
    EVENT_SCHEDULE_NOTIFY='schedule.notify',
    EVENT_SCHEDULE_LIST='schedule.list',
)


def default_account():
    return SERPLY_CONFIG.DEFAULT_ACCOUNT


def datetime_string():
    return datetime.today().isoformat()


def default_schedule_type():
    return SERPLY_CONFIG.SCHEDULE_TYPE_SERP


def default_domain_or_website():
    return 'domain'


def default_interval():
    return 'daily'


def default_source():
    return SERPLY_CONFIG.EVENT_SOURCE_SLACK


def get_parameter_name(key):
    return f'/serply/{STAGE}/{key.lower()}'


class Secrets:

    def __init__(self, ssm: object) -> None:
        self._ssm = ssm

    def get_parameter(self, key):
        try:
            response = self._ssm.get_parameter(
                Name=get_parameter_name(key),
                WithDecryption=True
            )
            value = response['Parameter']['Value']
        except Exception as e:
            print(str(e))
            value = ''
        return value

    def get(self, key):
        # Use .env or environment variable if available
        value = getenv(key)
        # Fallback to encrypted parameter store
        if value is None:
            value = self.get_parameter(key)
        return value
