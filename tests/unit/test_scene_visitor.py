# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
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
    assert turbine["name"] == "turbine_rect_1"

    assert "transform" in turbine
    assert "position" in turbine["transform"]
    assert "rotation" in turbine["transform"]
    assert "scale" in turbine["transform"]
    assert turbine["transform"]["position"] == [0, 0, 0]
    assert turbine["transform"]["rotation"] == [0, 0, 0]
    assert turbine["transform"]["scale"] == [1, 1, 1]

    assert len(turbine["children"]) == 0
