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


class SerplyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        RUNTIME = _lambda.Runtime.PYTHON_3_9
        DEFAULT_ACCOUNT = config['DEFAULT_ACCOUNT']
        STAGE = config['STAGE']
        SRC_DIR = config['SRC_DIR']
        SLACK_DIR = f'{SRC_DIR}/integration_slack'
        NOTIFICATIONS_DIR = f'{SRC_DIR}/notifications'
        LAYER_DIR = f'{SRC_DIR}/layer'

        lambda_layer = _lambda.LayerVersion(self, "SerplyLambdaLayer",
            code=_lambda.Code.from_asset(LAYER_DIR),
            compatible_runtimes=[RUNTIME],
            compatible_architectures=[
                _lambda.Architecture.X86_64, 
                _lambda.Architecture.ARM_64,
            ]
        )

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
            runtime=RUNTIME,
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
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(SLACK_DIR),
            handler='slack_respond_lambda.handler',
            timeout=Duration.seconds(5),
            # on_success=lambda_destinations.EventBridgeDestination(event_bus),
            environment={
                'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
                'STAGE': STAGE,
            },
        )

        notification_put_lambda = _lambda.Function(
            self, 'NotificationPutLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(NOTIFICATIONS_DIR),
            handler='notification_put_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            # on_success=lambda_destinations.EventBridgeDestination(event_bus),
            environment={
                'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
                'STAGE': STAGE,
            },
        )

        notification_serp_lambda = _lambda.Function(
            self, 'NotificationSerpLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(NOTIFICATIONS_DIR),
            handler='notification_serp_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'DEFAULT_ACCOUNT': DEFAULT_ACCOUNT,
                'STAGE': STAGE,
            },
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
                logging_level=apigateway.MethodLoggingLevel.INFO,
            ),
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

        notifications_dynamodb_table = dynamodb.Table(
            self, 'NotificationsDynamoDBTable',
            table_name=f'SerplyNotifications{STAGE.title()}',
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN if STAGE == 'prod' else RemovalPolicy.DESTROY,
        )
        
        notifications_dynamodb_table.grant_read_write_data(notification_put_lambda)
        notifications_dynamodb_table.grant_read_write_data(notification_serp_lambda)

        slack_command_event_rule = events.Rule(
            self, 'SlackCommandEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=["serply"],
                detail_type=[
                    'serp',
                    # 'search', # additional commands can be added
                ],
            ),
            targets=[
                events_targets.LambdaFunction(slack_respond_lambda),
                events_targets.LambdaFunction(notification_put_lambda),
            ],
        )
        
        slack_command_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        # rule = events.Rule(self, "Rule",
        #     schedule=events.Schedule.rate(cdk.Duration.minutes(1)),
        #     targets=[
        #         events_targets.LambdaFunction(destination),
        #     ],
        # )

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

        # notifications_dynamodb_table.grant_read_write_data(serp_lambda_function)
