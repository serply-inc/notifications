import logging
import json
import re
from dataclasses import asdict, dataclass, field
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


COMMAND = '/serply'
ICON_URL = 'https://avatars.githubusercontent.com/u/114946644?s=48&v=4'

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


# @app.event("app_mention")
# def handle_app_mentions(body, say, logger):
#     logger.info(body)
#     say("What's up?")


# @app.command(COMMAND)
def respond_to_slack_within_3_seconds(ack, respond, command):
    parser = SlackCommandParser(text=command['text'])
    valid_commands = ['serp']

    if parser.type not in valid_commands:
        ack(
            f'Please enter a valid command. Example: {COMMAND} serp google.com "google+search+api" daily')
        return
    elif parser.query == None:
        ack('A query is required in single or double quotes.')
        return
    else:
        ack()

    # blocks = [
    #     {
    #         'type': 'header',
    #         'text': {
    #             'type': 'plain_text',
    #             'text': f'{parser.type_name} Notification Scheduled {parser.interval.title()}',
    #             'emoji': True
    #         }
    #     },
    #     {
    #         'type': 'section',
    #         'fields': [
    #             {
    #                 'type': 'mrkdwn',
    #                 'text': f'*type:* {parser.type}'
    #             },
    #             {
    #                 'type': 'mrkdwn',
    #                 'text': f'*{parser.domain_or_website}:* {parser.domain if parser.domain else parser.website}'
    #             },
    #             {
    #                 'type': 'mrkdwn',
    #                 'text': f'*query:* {parser.query}'
    #             },
    #             {
    #                 'type': 'mrkdwn',
    #                 'text': f'*interval:* {parser.interval}'
    #             },
    #         ]
    #     },
    # ]

    # print(command['text'])
    # ack(blocks=blocks)


def run_long_process(respond, body):
    parser = SlackCommandParser(text=body['text'])

    blocks = [
        {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': f'{parser.type_name} Notification Scheduled {parser.interval.title()}',
                'emoji': True
            }
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f'*type:* {parser.type}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*{parser.domain_or_website}:* {parser.domain if parser.domain else parser.website}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*query:* {parser.query}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*interval:* {parser.interval}'
                },
            ]
        },
    ]
    
    metadata = json.dumps({
        'event_type': 'task_created',
        'event_payload': asdict(parser)
    })
    
    respond(
        blocks=blocks,
        response_type='in_channel',
        # replace_original=False,
        # metadata=metadata,
    )


app.command("/serply")(
    ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
    # unable to call `ack()` / can have multiple functions
    lazy=[run_long_process]
)


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

REGEX_COMMAND_TYPE = r'(serp)'
REGEX_INTERVAL = r'(test|daily|weekly|monthly)'
REGEX_DOMAIN = '[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}'


@dataclass
class SlackCommandParser:
    text: str
    type: str = field(init=False)
    type_name: str = field(init=False)
    website: str = field(init=False)
    domain: str = field(init=False)
    query: str = field(init=False)
    interval: str = field(init=False)
    domain_or_website: str = field(init=False)

    def _search(self, pattern, default_value=None):
        match = re.search(pattern, self.text)
        if match:
            return match[1] if match.lastindex and match.lastindex >= 1 else default_value
        return default_value

    def __post_init__(self):
        type_name_map = {'serp': 'SERP'}
        self.type = self._search(REGEX_COMMAND_TYPE, '')
        self.type_name = type_name_map.get(self.type)
        self.domain = self._search(
            rf'\|({REGEX_DOMAIN})>') if '|' in self.text else None
        self.website = self._search(
            rf'<(https?://{REGEX_DOMAIN})>') if 'http' in self.text else None
        self.query = re.sub(r'^q=', '', self._search(rf'["\'](.*)["\']'))
        self.interval = self._search(REGEX_INTERVAL, 'daily')
        self.domain_or_website = 'domain' if self.domain else 'website'


class SlackNotificationProvider(NotificationProvider):

    def configure(self, event: dict, context: dict):
        slack_handler = SlackRequestHandler(app=app)
        return slack_handler.handle(event, context)


# Examples

# def respond_to_slack_within_3_seconds(body, ack):
#     text = body.get("text")
#     if text is None or len(text) == 0:
#         ack(":x: Usage: /serply (description here)")
#     else:
#         ack(f"Accepted! (task: {body['text']})")

# import time
# def run_long_process(respond, body):
#     time.sleep(5)  # longer than 3 seconds
#     respond(f"Completed! (task: {body['text']})")

# app.command("/serply")(
#     ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
#     lazy=[run_long_process]  # unable to call `ack()` / can have multiple functions
# )
