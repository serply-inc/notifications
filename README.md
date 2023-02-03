# Serply.io Serverless Notifications
Serply.io + Slack + AWS + Python CDK

## Main Services
- Serply.io - SERP API
- Slack (Commands, Bolt)
- AWS CDK (Python)
- AWS API Gateway
- AWS Lambda (Python)
- AWS DynamoDB
- AWS EventBridge Scheduler
- AWS SSM Parameter Store

---

## Installation

```
cdk deploy --profile cloudchemy --outputs-file ./cdk.out/serply.outputs.json
```

## Generate Slack manifest

```
python3 install.py slack
```

## Install Slack app


## Set .env variables

```
AWS_PROFILE=acme
SERPLY_API_KEY=
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
```

## Store secrets on AWS SSM Parameter Store

```
python3 install.py secrets
```

## Slack Command Examples

### Creating a SERP Scheduled Notification

```yaml
/serply serp google.com "google+search" daily
```

---

## AWS CDK (Python)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


cdk synth --no-staging > template.yaml --profile cloudchemy