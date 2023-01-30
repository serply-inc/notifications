import json
from config import DEFAULT_ACCOUNT, DEFAULT_CORS_HEADERS
from datetime import datetime


def default_account():
    return DEFAULT_ACCOUNT


def datetime_string():
    return datetime.today().isoformat()


def get_challenge(body):
    if not body.startswith('{'):
        return False
    return json.loads(body).get('challenge', False)


def init_provider(
    provider_name: str,
    repository: object,
    secrets: object,
    serply: object,
):
    module_name = provider_name_to_module_name(provider_name)
    module = getattr(__import__(f'providers.{module_name}'), module_name)
    return getattr(module, provider_name_to_classname(provider_name))(
        repository=repository,
        secrets=secrets,
        serply=serply,
    )


def provider_name_to_classname(provider_name: str):
    return provider_name.replace('_', ' ').title().replace(' ', '') + 'NotificationProvider'


def provider_name_to_module_name(provider_name: str):
    return f'notification_provider_{provider_name}'


def success(data: dict, headers: dict = DEFAULT_CORS_HEADERS):
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(data),
    }
