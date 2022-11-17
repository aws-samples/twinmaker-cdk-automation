# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import pytest
from wind_farm.wind_farm import WindFarm, TurbineGroup


@pytest.fixture()
def farm():
    return WindFarm.load_from_yaml("tests/unit/farm.yaml", WindFarm)


def test_can_read_farm_file(farm):
    assert farm.name == "ACME WindFarm"
    assert farm.city == "Seattle"

    assert farm.urn.fqn == "urn:ngsi-ld:WindFarm:ACMEWindFarm"

    assert len(farm.items) == 2


def test_farm_has_turbine_groups(farm):
    group = farm.items[0]
    assert type(group) == TurbineGroup
    assert group.urn.fqn == "urn:ngsi-ld:TurbineGroup:group1"

    assert group.parent is not None
    assert group.parent == farm


def test_farm_has_turbine(farm):
    group = farm.items[0]
    assert len(group.items) == 2
    turbine = group.items[0]
    assert turbine.device_code == "0x01"
