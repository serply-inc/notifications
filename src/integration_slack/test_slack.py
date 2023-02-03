from dataclasses import asdict
from slack_api import SlackCommand
from slack_command_lambda import querystring_asdict
from urllib.parse import parse_qs

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


def test_querystring_asdict():

    expected_parse_qs = {
        'foo': ['bar']
    }

    assert parse_qs('foo=bar&bing=') == expected_parse_qs

    expected_querystring_asdict = {
        'foo': 'bar'
    }

    assert querystring_asdict('foo=bar&bing=') == expected_querystring_asdict
