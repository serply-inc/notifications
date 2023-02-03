from dataclasses import asdict
from integration_slack.api import SlackCommand

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


def test_slack_parse_command():
    for command, expected_dictionary in commands.items():
        command_dict = asdict(SlackCommand(command))
        for key in keys:
            assert command_dict.get(key) == expected_dictionary.get(key)
