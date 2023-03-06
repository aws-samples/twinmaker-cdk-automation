#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import aws_cdk as cdk
from cdk_nag import AwsSolutionsChecks
from aws_cdk import Aspects
from wind_farm.wind_farm_stack import WindFarmStack


app = cdk.App()
Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
WindFarmStack(app, "windfarm-sample")

app.synth()
