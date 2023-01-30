import json
from utils import success


def handler(event, context):

    print(json.dumps(event))

    return success({'ok': True})
