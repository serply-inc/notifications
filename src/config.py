from dotenv import load_dotenv
from os import getenv, path

load_dotenv()

DEFAULT_ACCOUNT = getenv('ACCOUNT', '98a64bf66ad64b7aa23227d882d91249')
STAGE = getenv('STAGE', 'dev')
SRC_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.dirname(SRC_DIR)

SECRET_NAMES = [
    'ACCOUNT',
    'SLACK_BOT_TOKEN',
    'SLACK_SIGNING_SECRET',
    'SERPLY_API_KEY',
]

DEFAULT_CORS_HEADERS = {
    "Access-Control-Allow-Headers": ','.join([
        'Content-Type',
        'X-Amz-Date',
        'Authorization',
        'X-Api-Key',
        'X-Amz-Security-Token',
        'X-Amz-User-Agent',
        'X-Slack-Signature',
    ]),
    "Access-Control-Allow-Methods": ','.join([
        'OPTIONS',
        'GET',
        'PUT',
        'POST',
        'DELETE',
        'PATCH',
        'HEAD',
    ]),
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
}
