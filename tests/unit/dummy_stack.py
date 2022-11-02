# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from os import path
from aws_cdk import Stack, aws_s3 as s3, aws_iottwinmaker as twinmaker

from constructs import Construct
from wind_farm.wind_farm import WindFarm, TwinMakerRoot
from wind_farm.visitors import WindFarmCDKVisitor


class DummyStack(Stack):
    """This is a dummy twinmaker stack that just provision a StefSite"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        filename: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        twinmaker_bucket = s3.Bucket(self, "Resources", bucket_name="resources")
        self.workspace = twinmaker.CfnWorkspace(
            self,
            "TwinMakerWorkspace",
            workspace_id="dummy_windfarm",
            role="arn:dummy",
            s3_location=twinmaker_bucket.bucket_arn,
        )

        farm = TwinMakerRoot.load_from_yaml(filename, WindFarm)

        visitor = WindFarmCDKVisitor(self, "WindFarm", self.workspace)
        farm.visit(visitor)
