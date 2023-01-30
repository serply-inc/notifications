#!/usr/bin/env python3
import sys
from src.services.secrets import Secrets
from src.config import STAGE, SECRET_NAMES

secrets = Secrets(STAGE, SECRET_NAMES)

if len(sys.argv) == 2 and sys.argv[1] == 'slack':
    secrets.slack_manifest()
elif len(sys.argv) == 2 and sys.argv[1] == 'secrets':
    secrets.ssm_put_parameters()
