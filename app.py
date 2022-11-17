#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import aws_cdk as cdk

from wind_farm.wind_farm_stack import WindFarmStack


app = cdk.App()
WindFarmStack(app, "windfarm-sample")

app.synth()
