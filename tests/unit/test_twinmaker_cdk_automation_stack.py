import aws_cdk as core
import aws_cdk.assertions as assertions

from wind_farm.wind_farm_stack import WindFarmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in twinmaker_cdk_automation/twinmaker_cdk_automation_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WindFarmStack(app, "twinmaker-cdk-automation")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
