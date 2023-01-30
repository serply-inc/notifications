import boto3
import json
from os import getenv, system
from pathlib import Path

ssm = boto3.client('ssm')


class Secrets:

    def __init__(self, stage_name: str, secret_names: list[str]) -> None:
        self._stage_name = stage_name
        self._secret_names = secret_names
        pass

    def get_secret_names(self):
        return self._secret_names

    def get_parameter_name(self, key):
        return f'/serply/{self._stage_name}/{key.lower()}'

    def get_parameter(self, key):
        try:
            response = ssm.get_parameter(
                Name=self.get_parameter_name(key),
                WithDecryption=True
            )
            value = response['Parameter']['Value']
        except Exception as e:
            print(str(e))
            value = ''
        return value

    def get(self, key):
        # Use .env or environment variable if available
        value = getenv(key)
        # Fallback to encrypted parameter store
        if value is None:
            value = self.get_parameter(key)
        return value

    def slack_manifest(self):
        outputs_file = open('cdk.out/serply.outputs.json')
        outputs = json.load(outputs_file)
        data = outputs[f'SerplyNotificationsStack{self._stage_name.title()}']

        API_URL: str
        for key, value in data.items():
            if key.startswith('SerplyNotificationsRestApiEndpoint'):
                API_URL = f'{value}notifications'

        manifest_file = Path('slack/slack_manifest.template.yaml')
        manifest_template = manifest_file.read_text()
        manifest = manifest_template.replace('API_URL', API_URL)

        manifest_filename = f'slack/slack_manifest.{self._stage_name}.yaml'

        file = open(manifest_filename, 'w+')
        file.write(manifest)
        file.close()
        
        print('Slack manifest saved: ' + manifest_filename)

    def ssm_put_parameters(self):
        aws_profile = None

        if getenv('AWS_PROFILE'):
            aws_profile = getenv('AWS_PROFILE')

        for secret_name in self._secret_names:

            command = [
                'aws ssm put-parameter --overwrite --type SecureString',
                f'--name "{self.get_parameter_name(secret_name)}"',
                f'--value "{getenv(secret_name)}"'
            ]

            command.append(f'--profile {aws_profile}')

            system(' '.join(command))

            print(
                f'SSM Parameter Store: {self.get_parameter_name(secret_name)}" stored successfully.'
            )
