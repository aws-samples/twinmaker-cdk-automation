# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

from email.mime import base
import pytest

from os import path
import aws_cdk as core
import aws_cdk.assertions as assertions
from wind_farm.wind_farm import TwinMakerRoot, WindFarm
from aws_cdk.assertions import Annotations, Match
from wind_farm.visitors import WindFarmSceneVisitor
from .dummy_stack import DummyStack
import json


@pytest.fixture()
def scene() -> str:
    farm = TwinMakerRoot.load_from_yaml("tests/unit/farm.yaml", WindFarm)

    visitor = WindFarmSceneVisitor(
        s3_bucket_name="test_bucket", base_file="tests/unit/base.json"
    )

    farm.visit(visitor)

    return json.loads(visitor.get_content())


def test_root(scene):

    assert "nodes" in scene
    assert len(scene["nodes"]) == 8

    windfarm = scene["nodes"][0]
    assert windfarm["name"] == "ACME WindFarm"

    assert "transform" in windfarm
    assert "position" in windfarm["transform"]
    assert "rotation" in windfarm["transform"]
    assert "scale" in windfarm["transform"]
    assert windfarm["transform"]["position"] == [0, 0, 0]
    assert windfarm["transform"]["rotation"] == [0, 0, 0]
    assert windfarm["transform"]["scale"] == [1, 1, 1]

    assert len(scene["rootNodeIndexes"]) == 1
    assert scene["rootNodeIndexes"][0] == 0


def test_turbine_group(scene):

    # TurbineGroup is a child of windfarm
    windfarm = scene["nodes"][0]
    assert len(windfarm["children"]) == 2
    assert windfarm["children"][0] == 1

    assert "nodes" in scene

    turbine_group = scene["nodes"][1]
    assert turbine_group["name"] == "group1"

    assert "transform" in turbine_group
    assert "position" in turbine_group["transform"]
    assert "rotation" in turbine_group["transform"]
    assert "scale" in turbine_group["transform"]
    assert turbine_group["transform"]["position"] == [0, 0, 0]
    assert turbine_group["transform"]["rotation"] == [0, 0, 0]
    assert turbine_group["transform"]["scale"] == [1, 1, 1]

    assert len(turbine_group["children"]) == 2


def test_turbine(scene):
    turbine = scene["nodes"][2]
    assert turbine["name"] == "turbine_1"

    assert "transform" in turbine
    assert "position" in turbine["transform"]
    assert "rotation" in turbine["transform"]
    assert "scale" in turbine["transform"]
    assert turbine["transform"]["position"] == [0, 0, 0]
    assert turbine["transform"]["rotation"] == [0, 0, 0]
    assert turbine["transform"]["scale"] == [1, 1, 1]

    assert "components" in turbine
    assert len(turbine["components"]) == 2
    assert (
        turbine["components"][0]["uri"]
        == "s3://test_bucket/models/animated_wind_turbine.glb"
    )

    assert len(turbine["children"]) == 0

    # The second turbine in the group shoud be automatically shifted
    turbine = scene["nodes"][3]
    assert turbine["name"] == "turbine_2"
    assert turbine["transform"]["position"] == [0, 0, 10]
    assert turbine["transform"]["scale"] == [1, 1, 1]

    # Verifying model shader
    model_shader = turbine["components"][1]
    assert model_shader["type"] == "ModelShader"
    assert model_shader["ruleBasedMapId"] == "turbineColorRule"

    data_binding_context = model_shader["valueDataBinding"]["dataBindingContext"]
    assert data_binding_context["entityId"] == "urn:ngsi-ld:Turbine:turbine_2"
    assert data_binding_context["componentName"] == "TurbineFan"
    assert data_binding_context["propertyName"] == "speed"
    assert data_binding_context["entityPath"] == "ACME WindFarm/group1/turbine_2"
