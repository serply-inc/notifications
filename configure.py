#!/usr/bin/env python3
import json
import sys
from serply_config import Config, get_parameter_name, STAGE
from dotenv import load_dotenv
from os import getenv, system
from pathlib import Path

load_dotenv(f'.env.{STAGE}')


def find_value_by_key_start(data: dict, start: str):
    return [v for k, v in data.items() if k.startswith(start)][0]


def slack_manifest(stage: str):
    outputs_file = open(f'cdk.out/serply_outputs_{stage}.json')
    outputs = json.load(outputs_file)
    data = outputs[f'SerplyNotificationsStack{stage.title()}']

    manifest_file = Path('src/slack/manifest.template.yaml')
    manifest_template = manifest_file.read_text()

    api_url = find_value_by_key_start(data, 'NotificationsRestApiEndpoint')

    manifest = manifest_template.replace(
        'API_URL', api_url + 'slack'
    ).replace(
        'STAGE', stage
    )

    manifest_filename = f'slack_manifest.{stage}.yaml'

    file = open(manifest_filename, 'w+')
    file.write(manifest)
    file.close()

    print('Slack manifest saved: ' + manifest_filename)


def ssm_put_parameters():

    aws_profile = getenv('AWS_PROFILE', 'default')

    for secret_name in Config.SECRET_NAMES:

        command = [
            'aws ssm put-parameter --overwrite --type SecureString',
            f'--name "{get_parameter_name(secret_name)}"',
            f'--value "{getenv(secret_name)}"'
        ]

        command.append(f'--profile {aws_profile}')

        system(' '.join(command))

        print(
            f'SSM Parameter Store: {get_parameter_name(secret_name)}" stored successfully.'
        )


if len(sys.argv) == 2 and sys.argv[1] == 'slack':
    slack_manifest(STAGE)

elif len(sys.argv) == 2 and sys.argv[1] == 'secrets':
    ssm_put_parameters()
