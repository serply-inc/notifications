import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk.serply_notifications_stack import SerplyNotificationsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serply_notifications/serply_notifications_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SerplyNotificationsStack(app, "serply-notifications")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
