# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

import pytest
from wind_farm.wind_farm import TurbineGroup, WindFarm


@pytest.fixture()
def farm():
    return WindFarm.load_from_yaml("tests/unit/farm.yaml", WindFarm)


def test_can_read_farm_file(farm):
    assert farm.name == "ACME WindFarm"
    assert len(farm.items) == 2

    assert farm.urn.fqn == "urn:ngsi-ld:WindFarm:ACMEWindFarm"


def test_farm_has_turbine_groups(farm):
    group = farm.items[0]
    assert type(group) == TurbineGroup
    assert group.shape == "rectangle"
    assert group.width == 2
    assert group.model is not None

    assert group.urn.fqn == "urn:ngsi-ld:TurbineGroup:group1"


def test_turbinegroup_has_parent(farm):
    group = farm.items[0]
    assert group.parent is not None
    assert group.parent == farm


def test_farm_has_turbine(farm):
    group = farm.items[0]
    assert len(group.items) == 2
    turbine = group.items[0]
    assert turbine.device_code == "0x01"
    assert turbine.parent.shape == "rectangle"
