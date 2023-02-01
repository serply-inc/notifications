# import boto3
# from config import STAGE, SECRET_NAMES
# from utils import init_provider
# from services.repositories import DynamoDBNotificationsRepository



# def default_account():
#     return getenv('ACCOUNT')

# def datetime_string():
#     return datetime.today().isoformat()

# @dataclass
# class Notification:
#     SK: str = field(init=False)
#     PK: str = field(init=False)
#     query: str = field(init=False)
#     domain: str = field(init=False)
#     website: str = field(init=False)
#     account: str = field(default_factory=default_account)
#     created_at: str = field(default_factory=datetime_string)
#     interval: str = 'daily'
#     provider: str = 'slack'

#     def __post_init__(self):
#         self.PK = f'notification_{self.account}'
#         self.SK = '#'.join([
#             self.PK,
#             f'interval_{self.interval}',
#             (f'website_{self.website}', f'domain_{self.domain}')[self.website],
#             f'query_{self.query}',
#         ])


# @dataclass
# class Serp:
#     SK: str = field(init=False)
#     PK: str = field(init=False)
#     query: str = field(init=False)
#     domain: str = field(init=False)
#     website: str = field(init=False)
#     account: str = field(default_factory=default_account)
#     created_at: str = field(default_factory=datetime_string)
#     interval: str = 'daily'
#     provider: str = 'slack'

#     def __post_init__(self):
#         self.PK = f'notification_{self.account}_serp'
#         self.SK = '#'.join([
#             self.PK,
#             f'interval_{self.interval}',
#             (f'website_{self.website}', f'domain_{self.domain}')[self.website],
#             f'query_{self.query}',
#         ])

# class SerplyNotifications:

#     def __init__(self, repository: object, secrets: object, serply: object) -> None:
#         self._repository = repository
#         self._secrets = secrets
#         self._serply = serply

#     def serp(self, notification_id: str):
#         print(notification_id)

#     def configure(self, event: dict, context: dict):
#         return self.get_provider('slack').configure(event, context)

#     def notify(self, notification_id: str):
#         # print(notification_type)
#         print(notification_id)

#     def get_provider(self, provider_name: str):
#         return init_provider(
#             provider_name=provider_name,
#             repository=self._repository,
#             secrets=self._secrets,
#             serply=self._serply,
#         )


# # def serply_notifications():
# #     secrets = serply_secrets()
# #     serply=Serply(secrets=secrets)
# #     dynamodb = boto3.resource('dynamodb')
# #     repository = DynamoDBNotificationsRepository(STAGE, dynamodb)
# #     return SerplyNotifications(
# #         repository=repository,
# #         secrets=secrets,
# #         serply=serply,
# #     )
    
# # def serply_secrets():
# #     return Secrets(boto3.client('ssm'), STAGE, SECRET_NAMES)