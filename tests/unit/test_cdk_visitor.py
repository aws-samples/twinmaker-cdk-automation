# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import pytest

from os import path
import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk.assertions import Annotations, Match

from .dummy_stack import DummyStack


@pytest.fixture()
def stack() -> DummyStack:
    app = core.App()
    _stack = DummyStack(app, "test", filename="tests/unit/farm.yaml")
    return _stack


def test_root(stack):
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::IoTTwinMaker::Entity",
        {
            "EntityName": "ACME WindFarm",
            "EntityId": "urn:ngsi-ld:WindFarm:ACMEWindFarm",
            "Components": {},
        },
    )
