#!/usr/bin/env python3
from os import system
from serply_config import AWS_PROFILE, STAGE

system(f'cdk deploy --profile {AWS_PROFILE} --outputs-file ./cdk.out/serply_outputs_{STAGE}.json')

