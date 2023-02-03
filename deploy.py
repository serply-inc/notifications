#!/usr/bin/env python3
from os import system
from serply_config import SERPLY_CONFIG

system(f'cdk deploy --profile {SERPLY_CONFIG.AWS_PROFILE} --outputs-file ./cdk.out/serply_outputs_{SERPLY_CONFIG.STAGE}.json')

