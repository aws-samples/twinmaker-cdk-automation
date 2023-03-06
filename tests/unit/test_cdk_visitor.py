# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import pytest

import aws_cdk as core
import aws_cdk.assertions as assertions

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


def test_turbine_group(stack):
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::IoTTwinMaker::Entity",
        {
            "EntityName": "group1",
            "EntityId": "urn:ngsi-ld:TurbineGroup:group1",
            "ParentEntityId": "urn:ngsi-ld:WindFarm:ACMEWindFarm",
            "Components": {},
        },
    )


def test_turbine(stack):
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::IoTTwinMaker::Entity",
        {
            "EntityName": "turbine_rect_1",
            "EntityId": "urn:ngsi-ld:Turbine:turbine_rect_1",
            "ParentEntityId": "urn:ngsi-ld:TurbineGroup:group1",
            "Components": {},
        },
    )
