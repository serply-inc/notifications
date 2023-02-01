import ssl
from dataclasses import asdict

ssl._create_default_https_context = ssl._create_unverified_context

from providers.notification_provider_slack import SlackCommandParser

def test_slack_parse_command():

    commands = {
        'serp <http://google.com|google.com> "q=foo+bar"': {
            'type': 'serp',
            'domain': 'google.com',
            'website': None,
            'query': 'foo+bar',
            'interval': 'daily',
        },
        'serp <http://google.com> "foo+bar"': {
            'type': 'serp',
            'domain': None,
            'website': 'http://google.com',
            'query': 'foo+bar',
            'interval': 'daily',
        },
        'serp <http://google.com> "foo+bar" daily': {
            'type': 'serp',
            'domain': None,
            'website': 'http://google.com',
            'query': 'foo+bar',
            'interval': 'daily',
        },
        'serp <http://google.com> "foo+bar" weekly': {
            'type': 'serp',
            'domain': None,
            'website': 'http://google.com',
            'query': 'foo+bar',
            'interval': 'weekly',
        },
        'serp <http://google.com> "foo+bar" monthly': {
            'type': 'serp',
            'domain': None,
            'website': 'http://google.com',
            'query': 'foo+bar',
            'interval': 'monthly',
        },
    }

    keys = [
        'type',
        'domain',
        'website',
        'query',
        'interval',
    ]

    for command, expected_dictionary in commands.items():
        command_dict = asdict(SlackCommandParser(command))
        for key in keys:
            assert command_dict.get(key) == expected_dictionary.get(key)
