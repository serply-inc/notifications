from services.notifications import serply_notifications
from utils import success

notifications = serply_notifications()


def handler(event, context):
    notification = {
        'query': 'serp+api',
        'domain': 'serply.io',
        'website': '',
        'provider': 'slack',
        'interval': 'daily',
    }

    # @todo add try catch
    notifications.save_serp(notification)

    return success({'ok': True})
