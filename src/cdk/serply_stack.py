from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_scheduler as scheduler,
    Duration,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
from serply_config import SerplyConfig


class SerplyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: SerplyConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        RUNTIME = _lambda.Runtime.PYTHON_3_9

        lambda_layer = _lambda.LayerVersion(
            self, f'{config.STACK_NAME}LambdaLayer{config.STAGE_SUFFIX}',
            code=_lambda.Code.from_asset(config.LAYER_DIR),
            compatible_runtimes=[RUNTIME],
            compatible_architectures=[
                _lambda.Architecture.X86_64,
                _lambda.Architecture.ARM_64,
            ]
        )

        event_bus = events.EventBus(
            self, config.EVENT_BUS_NAME,
            event_bus_name=config.EVENT_BUS_NAME,
        )

        event_bus.apply_removal_policy(RemovalPolicy.DESTROY)

        scheduler_managed_policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            'AmazonEventBridgeSchedulerFullAccess'
        )

        scheduler_role = iam.Role(
            self, 'SerplySchedulerRole',
            assumed_by=iam.ServicePrincipal('scheduler.amazonaws.com'),
        )
        
        scheduler_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=['lambda:InvokeFunction'],
                resources=['*'],
            )
        )

        slack_receive_lambda = _lambda.Function(
            self, 'SlackCommandLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.SLACK_DIR),
            handler='slack_receive_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )

        event_bus.grant_put_events_to(slack_receive_lambda)

        slack_respond_lambda = _lambda.Function(
            self, 'SlackRespondLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.SLACK_DIR),
            handler='slack_respond_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'SLACK_BOT_TOKEN': config.SLACK_BOT_TOKEN,
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )

        slack_notify_lambda = _lambda.Function(
            self, 'SlackNotifyLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.SLACK_DIR),
            handler='slack_notify_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'SLACK_BOT_TOKEN': config.SLACK_BOT_TOKEN,
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )

        slack_notify_lambda.role.add_managed_policy(scheduler_managed_policy)

        schedule_target_lambda = _lambda.Function(
            self, 'NotificationSerpLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.NOTIFICATIONS_DIR),
            handler='schedule_target_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'SERPLY_API_KEY': config.SERPLY_API_KEY,
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )
        
        event_bus.grant_put_events_to(schedule_target_lambda)

        schedule_save_lambda = _lambda.Function(
            self, 'NotificationPutLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.NOTIFICATIONS_DIR),
            handler='schedule_save_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'SCHEDULE_TARGET_ARN': schedule_target_lambda.function_arn,
                'SCHEDULE_ROLE_ARN': scheduler_role.role_arn,
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )

        schedule_save_lambda.role.add_managed_policy(scheduler_managed_policy)

        schedule_disable_lambda = _lambda.Function(
            self, 'ScheduleDisableLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.NOTIFICATIONS_DIR),
            handler='schedule_disable_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )
        
        schedule_disable_lambda.role.add_managed_policy(scheduler_managed_policy)

        schedule_enable_lambda = _lambda.Function(
            self, 'ScheduleEnableLambdaFunction',
            runtime=RUNTIME,
            code=_lambda.Code.from_asset(config.NOTIFICATIONS_DIR),
            handler='schedule_enable_lambda.handler',
            timeout=Duration.seconds(5),
            layers=[lambda_layer],
            environment={
                'SCHEDULE_TARGET_ARN': schedule_target_lambda.function_arn,
                'SCHEDULE_ROLE_ARN': scheduler_role.role_arn,
                'STACK_NAME': config.STACK_NAME,
                'STAGE': config.STAGE,
            },
        )
        
        schedule_enable_lambda.role.add_managed_policy(scheduler_managed_policy)

        slack_save_event_rule = events.Rule(
            self, 'SlackCommandEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=[config.EVENT_SOURCE_SLACK],
                detail_type=[
                    config.EVENT_SCHEDULE_SAVE,
                ],
            ),
            targets=[
                events_targets.LambdaFunction(schedule_save_lambda),
                events_targets.LambdaFunction(slack_respond_lambda),
            ],
        )

        slack_save_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        slack_list_event_rule = events.Rule(
            self, 'SlackListEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=[config.EVENT_SOURCE_SLACK],
                detail_type=[
                    config.EVENT_SCHEDULE_LIST,
                ],
            ),
            targets=[
                events_targets.LambdaFunction(slack_respond_lambda),
            ],
        )

        slack_list_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        slack_notify_event_rule = events.Rule(
            self, 'SlackNotifyEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=[config.EVENT_SOURCE_SLACK],
                detail_type=[
                    config.EVENT_SCHEDULE_NOTIFY,
                ],
            ),
            targets=[
                events_targets.LambdaFunction(slack_notify_lambda),
            ],
        )

        slack_notify_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        slack_disable_event_rule = events.Rule(
            self, 'SlackDisableEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=[config.EVENT_SOURCE_SLACK],
                detail_type=[
                    config.EVENT_SCHEDULE_DISABLE,
                ],
            ),
            targets=[
                events_targets.LambdaFunction(schedule_disable_lambda),
                events_targets.LambdaFunction(slack_respond_lambda),
            ],
        )

        slack_disable_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        slack_enable_event_rule = events.Rule(
            self, 'SlackEnableEventRule',
            event_bus=event_bus,
            event_pattern=events.EventPattern(
                source=[config.EVENT_SOURCE_SLACK],
                detail_type=[
                    config.EVENT_SCHEDULE_ENABLE,
                ],
            ),
            targets=[
                events_targets.LambdaFunction(schedule_enable_lambda),
                events_targets.LambdaFunction(slack_respond_lambda),
            ],
        )

        slack_enable_event_rule.apply_removal_policy(RemovalPolicy.DESTROY)

        cors_options = apigateway.CorsOptions(
            allow_origins=apigateway.Cors.ALL_ORIGINS,
            allow_methods=apigateway.Cors.ALL_METHODS,
            allow_credentials=True,
        )

        rest_api = apigateway.RestApi(
            self, f'NotificationsRestApi',
            default_cors_preflight_options=cors_options,
            endpoint_export_name=f'NotificationsRestApiUrl{config.STAGE_SUFFIX}',
            cloud_watch_role=True,
            deploy_options=apigateway.StageOptions(
                stage_name=config.STAGE,
                data_trace_enabled=True,
                logging_level=apigateway.MethodLoggingLevel.INFO,
            ),
        )

        slack_receive_lambda_integration = apigateway.LambdaIntegration(
            handler=slack_receive_lambda,
        )

        rest_api_resource = rest_api.root.add_resource('slack')

        rest_api_resource_proxy = rest_api_resource.add_proxy(
            default_integration=slack_receive_lambda_integration,
            any_method=True,
        )

        rest_api_method = rest_api_resource.add_method(
            http_method='POST',
            integration=slack_receive_lambda_integration,
        )

        dynamodb_table = dynamodb.Table(
            self, config.NOTIFICATION_TABLE_NAME,
            table_name=config.NOTIFICATION_TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN if config.STAGE == 'prod' else RemovalPolicy.DESTROY,
        )
        
        dynamodb_table.add_global_secondary_index(
            index_name='CollectionIndex',
            partition_key=dynamodb.Attribute(
                name="collection",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING,
            ),
        )

        dynamodb_table.grant_read_write_data(schedule_disable_lambda)
        dynamodb_table.grant_read_write_data(schedule_enable_lambda)
        dynamodb_table.grant_read_write_data(schedule_save_lambda)
        dynamodb_table.grant_read_write_data(schedule_target_lambda)
        dynamodb_table.grant_read_data(slack_respond_lambda)

        schedule_group = scheduler.CfnScheduleGroup(
            self, config.SCHEDULE_GROUP_NAME,
            name=config.SCHEDULE_GROUP_NAME,
        )

        # ssm_inline_policy = iam.Policy(
        #     self, 'NotificationsSSMParametersReadPolicy',
        #     statements=[
        #         iam.PolicyStatement(
        #             actions=['ssm:GetParameter'],
        #             resources=[f'arn:aws:ssm:*:*:parameter/serply/{STAGE}/*'],
        #         )
        #     ]
        # )

        # slack_receive_lambda_function.role.attach_inline_policy(ssm_inline_policy)
        # serp_lambda_function.role.attach_inline_policy(ssm_inline_policy)
