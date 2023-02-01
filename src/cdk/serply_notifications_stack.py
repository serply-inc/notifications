from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_lambda as _lambda,
    aws_lambda_destinations as lambda_destinations,
    aws_lambda_event_sources as lambda_event_sources,
    aws_iam as iam,
    aws_sns as sns,
    aws_sqs as sqs,
    Duration,
    RemovalPolicy,
    Stack,
)
from constructs import Construct


class SerplyNotificationsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # @todo Add tags

        DEFAULT_ACCOUNT = config['DEFAULT_ACCOUNT']
        STAGE = config['STAGE']
        SRC_DIR = config['SRC_DIR']
        SLACK_DIR = f'{SRC_DIR}/integration_slack'
        SERPLY_DIR = f'{SRC_DIR}/serply'


        event_bus = events.EventBus(
            self, 'NotificationsEventBus', 
            event_bus_name=f'NotificationsEventBus{STAGE.title()}',
        )
        event_bus.apply_removal_policy(RemovalPolicy.DESTROY)
        event_bus_put_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW, 
            resources=['*'], 
            actions=['events:PutEvents'],
        )

        slack_command_lambda = _lambda.Function(
            self, 'SlackCommandLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(SLACK_DIR),
            handler='slack_command_lambda.handler',
            timeout=Duration.seconds(5),
            environment={
                'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
                'STAGE': STAGE,
            },
        )
        
        slack_command_lambda.add_to_role_policy(event_bus_put_policy)

        slack_respond_lambda = _lambda.Function(
            self, 'SlackRespondLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(SLACK_DIR),
            handler='slack_respond_lambda.handler',
            timeout=Duration.seconds(5),
            # on_success=lambda_destinations.EventBridgeDestination(event_bus),
            environment={
                'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
                'STAGE': STAGE,
            },
        )

        # slack_notification_put_lambda = _lambda.Function(
        #     self, 'SlackNotificationPutLambdaFunction',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset(SLACK_DIR),
        #     handler='slack_notification_put_lambda.handler',
        #     timeout=Duration.seconds(5),
        #     # on_success=lambda_destinations.EventBridgeDestination(event_bus),
        #     environment={
        #         'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
        #         'STAGE': STAGE,
        #     },
        # )

        # slack_command_lambda_function = _lambda.Function(
        #     self, 'NotificationsConfigureLambdaFunction',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset(SRC_DIR),
        #     handler='lambda_configure.handler',
        #     timeout=Duration.seconds(10),
        # environment={
        #     'SLACK_BOT_TOKEN': getenv('SLACK_BOT_TOKEN'),
        #     'SLACK_SIGNING_SECRET': getenv('SLACK_SIGNING_SECRET'),
        #     'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
        #     'STAGE': STAGE,
        # },
        #     on_success=lambda_destinations.LambdaDestination(save_lambda_function)
        # )

        # slack_command_lambda_function = _lambda.Function(
        #     self, 'NotificationsConfigureLambdaFunction',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset('slack'),
        #     handler='lambda_slack.handler',
        #     timeout=Duration.seconds(5),
        #     on_success=lambda_destinations.LambdaDestination(save_lambda_function),
        #     # environment={
        #     #     'SLACK_BOT_TOKEN': getenv('SLACK_BOT_TOKEN'),
        #     #     # 'SLACK_SIGNING_SECRET': getenv('SLACK_SIGNING_SECRET'),
        #     #     'STAGE': STAGE
        #     # },
        # )

        # serp_lambda_function = _lambda.Function(
        #     self, 'NotificationsSerpLambdaFunction',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset(SRC_DIR),
        #     handler='lambda_serp.handler',
        #     timeout=Duration.seconds(10),
        # )

        # notify_lambda_function = _lambda.Function(
        #     self, 'NotificationsNotifyLambdaFunction',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset(SRC_DIR),
        #     handler='lambda_notify.handler',
        #     timeout=Duration.seconds(3),
        # )

        # notifications_dynamodb_table = dynamodb.Table(
        #     self, 'NotificationsDynamoDBTable',
        #     table_name=f'Notifications-{STAGE}',
        #     partition_key=dynamodb.Attribute(
        #         name='PK',
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        #     sort_key=dynamodb.Attribute(
        #         name='SK',
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        #     billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        #     removal_policy=RemovalPolicy.RETAIN,
        # )

        slack_command_event_rule = events.Rule(
            self, 'SlackCommandEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=["serply"],
                detail_type=['serp'],
            )
        )
        
        slack_command_event_rule.add_target(
            events_targets.LambdaFunction(slack_respond_lambda)
        )

        cors_options = apigateway.CorsOptions(
            allow_origins=apigateway.Cors.ALL_ORIGINS,
            allow_methods=apigateway.Cors.ALL_METHODS,
            allow_credentials=True,
        )

        rest_api = apigateway.RestApi(
            self, 'NotificationsRestApi',
            default_cors_preflight_options=cors_options,
            endpoint_export_name=f'NotificationsRestApiUrl{STAGE.title()}',
            cloud_watch_role=True,
            deploy_options=apigateway.StageOptions(
                stage_name=STAGE,
                data_trace_enabled=True,
                # metrics_enabled=True,
                logging_level=apigateway.MethodLoggingLevel.INFO,
            ),
            # policy = iam.Policy(
            #     self, 'NotificationsRestApiPolicy',
            #     statements=[
            #         iam.PolicyDocument(
            #             actions=['*'],
            #             resources=['AWS::ApiGateway::Account'],
            #         ),
            #         iam.PolicyStatement(
            #             actions=[''],
            #             principals=[iam.AccountRootPrincipal()],
            #             resources=['*"]
            #         )
            #     ]
            # )
        )

        slack_command_lambda_integration = apigateway.LambdaIntegration(
            handler=slack_command_lambda,
        )

        rest_api_resource = rest_api.root.add_resource('slack')

        rest_api_resource_proxy = rest_api_resource.add_proxy(
            default_integration=slack_command_lambda_integration,
            any_method=True,
        )

        rest_api_method = rest_api_resource.add_method(
            http_method='POST',
            integration=slack_command_lambda_integration,
        )

        # slack_command_lambda_function.role.attach_inline_policy(lazy_lambda_invocation_inline_policy)

        # ssm_inline_policy = iam.Policy(
        #     self, 'NotificationsSSMParametersReadPolicy',
        #     statements=[
        #         iam.PolicyStatement(
        #             actions=['ssm:GetParameter'],
        #             resources=[f'arn:aws:ssm:*:*:parameter/serply/{STAGE}/*'],
        #         )
        #     ]
        # )

        # slack_command_lambda_function.role.attach_inline_policy(ssm_inline_policy)
        # serp_lambda_function.role.attach_inline_policy(ssm_inline_policy)
        # notify_lambda_function.role.attach_inline_policy(ssm_inline_policy)

        # notifications_dynamodb_table.grant_read_write_data(slack_command_lambda_function)
        # notifications_dynamodb_table.grant_read_write_data(serp_lambda_function)
        # notifications_dynamodb_table.grant_read_data(notify_lambda_function)
