# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import pytest
from wind_farm.wind_farm import WindFarm


@pytest.fixture()
def farm():
    return WindFarm.load_from_yaml("tests/unit/farm.yaml", WindFarm)


def test_can_read_farm_file(farm):
    assert farm.name == "ACME WindFarm"
