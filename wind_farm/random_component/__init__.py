# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pkgutil import get_loader
from time import time
from aws_cdk import (
    aws_lambda as lambda_,
    aws_iottwinmaker as twinmaker,
    aws_iam as iam,
    Duration,
    aws_logs as logs,
    Stack,
)


from aws_cdk.aws_lambda_python_alpha import PythonFunction, PythonLayerVersion
from constructs import Construct
from os import path


class RandomTwinMakerComponent(Construct):

    TYPE = "com.aws.sample.component.random"

    def lambda_name():
        return "windfarm-sample-random-read"

    def __init__(
        self,
        scope: Construct,
        id: str,
        workspace_id: str,
        *,
        prefix=None,
    ):
        super().__init__(scope, id)

        region = Stack.of(self).region
        account = Stack.of(self).account

        # Role needed to access TimeStream DB
        lambda_name = RandomTwinMakerComponent.lambda_name()
        lambda_role = iam.Role(
            self,
            "RandomComponentLambdaRole",
            role_name="windfarm-sample-random-component-lambda-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "timeStreamReadOnly": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            resources=[
                                f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/{lambda_name}:*",
                                f"arn:aws:logs:{region}:{account}:log-group:/aws/lambda/{lambda_name}",
                            ],
                            effect=iam.Effect.ALLOW,
                        ),
                    ]
                )
            },
        )

        dir_path = path.dirname(path.realpath(__file__))
        lambda_data_read = PythonFunction(
            self,
            "RandomComponentLambda",
            function_name=RandomTwinMakerComponent.lambda_name(),
            entry=path.join(dir_path, "lambda_code"),
            layers=[
                PythonLayerVersion(
                    self,
                    "udq_utils_layers",
                    entry=path.join(dir_path, "udq_helper_utils"),
                    compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
                )
            ],
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="handler.py",
            handler="lambda_handler",
            memory_size=256,
            role=lambda_role,
            timeout=Duration.minutes(15),
            log_retention=logs.RetentionDays.ONE_DAY,
            environment={},
        )

        twinmaker.CfnComponentType(
            self,
            "RandomComponentType",
            component_type_id=self.TYPE,
            workspace_id=workspace_id,
            functions={
                "dataReader": {
                    "implementedBy": {
                        "lambda": {"arn": lambda_data_read.function_arn},
                        "isNative": False,
                    },
                    "isInherithed": False,
                }
            },
            property_definitions={
                "min": {
                    "dataType": {"type": "DOUBLE"},
                    "isTimeSeries": False,
                    "isRequiredInEntity": True,
                    "isExternalId": False,
                    "isStoredExternally": False,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": False,
                },
                "max": {
                    "dataType": {"type": "DOUBLE"},
                    "isTimeSeries": False,
                    "isRequiredInEntity": True,
                    "isExternalId": False,
                    "isStoredExternally": False,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": False,
                },
                "speed": {
                    "dataType": {"type": "DOUBLE"},
                    "isTimeSeries": True,
                    "isRequiredInEntity": False,
                    "isExternalId": False,
                    "isStoredExternally": True,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": False,
                },
            },
        )
