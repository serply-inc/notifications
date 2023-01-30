import boto3
from config import STAGE, SECRET_NAMES
from utils import init_provider
from services.repositories import DynamoDBNotificationsRepository
from services.serply import Serply
from services.secrets import Secrets

class SerplyNotifications:

    def __init__(self, repository: object, secrets: object, serply: object) -> None:
        self._repository = repository
        self._secrets = secrets
        self._serply = serply

    def serp(self, notification_id: str):
        print(notification_id)

    def configure(self, event: dict, context: dict):
        return self.get_provider('slack').configure(event, context)

    def notify(self, notification_id: str):
        # print(notification_type)
        print(notification_id)

    def get_provider(self, provider_name: str):
        return init_provider(
            provider_name=provider_name,
            repository=self._repository,
            secrets=self._secrets,
            serply=self._serply,
        )


def serply_notifications():
    secrets = serply_secrets()
    serply=Serply(secrets=secrets)
    dynamodb = boto3.resource('dynamodb')
    repository = DynamoDBNotificationsRepository(STAGE, dynamodb)
    return SerplyNotifications(
        repository=repository,
        secrets=secrets,
        serply=serply,
    )
    
def serply_secrets():
    return Secrets(STAGE, SECRET_NAMES)