import json
# from api import SlackClient
# from messages import SerpNotificationMessage
# from os import getenv

# slack = SlackClient(getenv('SLACK_BOT_TOKEN'))


def handler(event, context):
    
    print(json.dumps(event))

    # detail = event.get('detail')
    # response_url = detail.get('response_url')
    # command = detail.get('command')

    # # @todo respond with "Please enter a valid command" when invalid

    # message = SerpNotificationMessage(
    #     channel_id=detail.get('channel_id'),
    #     domain=command.get('domain'),
    #     domain_or_website=command.get('domain_or_website'),
    #     interval=command.get('interval'),
    #     query=command.get('query'),
    #     type=command.get('type'),
    #     type_name=command.get('type_name'),
    #     user_id=detail.get('user_id'),
    #     website=command.get('website'),
    # )

    # return slack.notify(response_url, message)

    return {'ok': True}
