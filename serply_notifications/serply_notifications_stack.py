from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_lambda_destinations as destinations,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class SerplyNotificationsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, serply_config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_name = serply_config['stage']
        src_dir = serply_config['src_dir']

        save_lambda_function = _lambda.Function(
            self, 'SerplySaveLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(src_dir),
            handler='lambda_save.handler',
            timeout=Duration.seconds(3),
        )

        configure_lambda_function = _lambda.Function(
            self, 'SerplyConfigureLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(src_dir),
            handler='lambda_configure.handler',
            timeout=Duration.seconds(10),
            environment={
                'SLACK_BOT_TOKEN': getenv('SLACK_BOT_TOKEN'),
                'SLACK_SIGNING_SECRET': getenv('SLACK_SIGNING_SECRET'),
                'STAGE': stage_name
            },
            on_success=destinations.LambdaDestination(
                save_lambda_function,
                response_only=True,
            )
        )

        serp_lambda_function = _lambda.Function(
            self, 'SerplySerpLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(src_dir),
            handler='lambda_serp.handler',
            timeout=Duration.seconds(10),
        )

        notify_lambda_function = _lambda.Function(
            self, 'SerplyNotifyLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(src_dir),
            handler='lambda_notify.handler',
            timeout=Duration.seconds(3),
        )

        notifications_dynamodb_table = dynamodb.Table(
            self, 'SerplyNotificationsDynamoDBTable',
            table_name=f'SerplyNotifications-{stage_name}',
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
        )
        
        cors_options = apigateway.CorsOptions(
            allow_origins=apigateway.Cors.ALL_ORIGINS,
            allow_methods=apigateway.Cors.ALL_METHODS,
            allow_credentials=True,
        )
        
        notifications_rest_api = apigateway.RestApi(
            self, 'SerplyNotificationsRestApi',
            default_cors_preflight_options=cors_options,
            endpoint_export_name=f'SerplyNotificationsRestApiUrl{stage_name.title()}',
            deploy_options=apigateway.StageOptions(
                stage_name=stage_name,
            ),
        )

        configure_lambda_integration = apigateway.LambdaIntegration(
            handler=configure_lambda_function,
        )

        notifications_rest_api_resource = notifications_rest_api.root.add_resource('notifications')

        notifications_rest_api_resource_proxy = notifications_rest_api_resource.add_proxy(
            default_integration=configure_lambda_integration,
            any_method=True,
        )

        configure_rest_api_method = notifications_rest_api_resource.add_method(
            http_method='POST', 
            integration=configure_lambda_integration,
        )
        
        lazy_lambda_invocation_inline_policy = iam.Policy(
            self, 'SerplyLazyLambdaInvocationPolicy',
            statements=[
                iam.PolicyStatement(
                    actions=['lambda:InvokeFunction', 'lambda:GetFunction'],
                    resources=['*'],
                )
            ]
        )

        configure_lambda_function.role.attach_inline_policy(lazy_lambda_invocation_inline_policy)
        
        ssm_inline_policy = iam.Policy(
            self, 'SerplySSMParametersReadPolicy',
            statements=[
                iam.PolicyStatement(
                    actions=['ssm:GetParameter'],
                    resources=[f'arn:aws:ssm:*:*:parameter/serply/{stage_name}/*'],
                )
            ]
        )
        
        configure_lambda_function.role.attach_inline_policy(ssm_inline_policy)
        serp_lambda_function.role.attach_inline_policy(ssm_inline_policy)
        notify_lambda_function.role.attach_inline_policy(ssm_inline_policy)

        notifications_dynamodb_table.grant_read_write_data(configure_lambda_function)
        notifications_dynamodb_table.grant_read_write_data(serp_lambda_function)
        notifications_dynamodb_table.grant_read_data(notify_lambda_function)
