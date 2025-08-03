import aws_cdk as core
import aws_cdk.assertions as assertions

from earningspy_cdk.stacks.earningspy_s3_stack import EarningspyCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in earningspy_cdk/earningspy_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EarningspyCdkStack(app, "earningspy-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
