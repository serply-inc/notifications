#!/usr/bin/env python3
import json
import sys
from serply_config import get_parameter_name, SERPLY_CONFIG
from os import getenv, system
from pathlib import Path


def find_value_by_key_start(data: dict, start: str):
    return [v for k, v in data.items() if k.startswith(start)][0]


def slack_manifest():
    outputs_file = open(f'cdk.out/serply_outputs_{SERPLY_CONFIG.STAGE}.json')
    outputs = json.load(outputs_file)
    data = outputs[SERPLY_CONFIG.STACK_NAME_FULL]

    manifest_file = Path('src/integration_slack/manifest.template.yaml')
    manifest_template = manifest_file.read_text()

    api_url = find_value_by_key_start(data, f'NotificationsRestApi{SERPLY_CONFIG.STAGE_SUFFIX}Endpoint')

    manifest = manifest_template.replace(
        'API_URL', api_url + 'slack'
    ).replace(
        'STAGE', SERPLY_CONFIG.STAGE
    )

    manifest_filename = f'slack_manifest.{SERPLY_CONFIG.STAGE}.yaml'

    file = open(manifest_filename, 'w+')
    file.write(manifest)
    file.close()

    print('Slack manifest saved: ' + manifest_filename)


def ssm_put_parameters():

    for secret_name in SERPLY_CONFIG.SECRET_KEYS:

        command = [
            'aws ssm put-parameter --overwrite --type SecureString',
            f'--name "{get_parameter_name(secret_name)}"',
            f'--value "{getenv(secret_name)}"'
        ]

        command.append(f'--profile {SERPLY_CONFIG.AWS_PROFILE}')

        system(' '.join(command))

        print(
            f'SSM Parameter Store: {get_parameter_name(secret_name)}" stored successfully.'
        )


if len(sys.argv) == 2 and sys.argv[1] == 'slack':
    slack_manifest()

elif len(sys.argv) == 2 and sys.argv[1] == 'secrets':
    ssm_put_parameters()
