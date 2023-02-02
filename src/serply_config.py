from datetime import datetime
from dotenv import load_dotenv
from os import getenv, path

STAGE = getenv('STAGE', 'dev')

load_dotenv(f'.env.{STAGE}')


AWS_PROFILE = getenv('AWS_PROFILE', 'default')
DEFAULT_ACCOUNT = getenv('ACCOUNT', '98a64bf66ad64b7aa23227d882d91249')
SRC_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.dirname(SRC_DIR)
SERPLY_API_KEY = getenv('SERPLY_API_KEY')


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

# DEFAULT_CORS_HEADERS = {
#     "Access-Control-Allow-Headers": ','.join([
#         'Content-Type',
#         'X-Amz-Date',
#         'Authorization',
#         'X-Api-Key',
#         'X-Amz-Security-Token',
#         'X-Amz-User-Agent',
#         'X-Slack-Signature',
#     ]),
#     "Access-Control-Allow-Methods": ','.join([
#         'OPTIONS',
#         'GET',
#         'PUT',
#         'POST',
#         'DELETE',
#         'PATCH',
#         'HEAD',
#     ]),
#     'Access-Control-Allow-Origin': '*',
#     'Content-Type': 'application/json',
# }


def get_parameter_name(key):
    return f'/serply/{STAGE}/{key.lower()}'


class Config:

    SECRET_NAMES = [
        'ACCOUNT',
        'SLACK_BOT_TOKEN',
        'SLACK_SIGNING_SECRET',
        'SERPLY_API_KEY',
    ]

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
