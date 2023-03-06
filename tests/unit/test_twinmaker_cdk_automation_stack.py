# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import aws_cdk as core
from aws_cdk.assertions import Match, Annotations

from cdk_nag import AwsSolutionsChecks
from aws_cdk import Aspects

from wind_farm.wind_farm_stack import WindFarmStack


def test_nag_has_no_error():
    app = core.App()
    Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
    stack = WindFarmStack(app, "twinmaker-cdk-automation")

    errors = Annotations.from_stack(stack).find_error(
        "*", Match.string_like_regexp("AwsSolutions-.*")
    )

    assert len(errors) == 0
