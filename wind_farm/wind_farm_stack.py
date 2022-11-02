# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct


class WindFarmStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TwinmakerCdkAutomationQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
