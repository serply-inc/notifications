from services.notifications import serply_notifications
from utils import get_challenge, success

notifications = serply_notifications()


def handler(event, context):
    challenge = get_challenge(event.get('body'))

    if challenge:
        return success({
            'challenge': challenge
        })

    response = notifications.configure(
        event=event,
        context=context,
    )

    print(response)

    return response
