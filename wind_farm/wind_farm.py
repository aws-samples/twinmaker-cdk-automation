# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0


from twinmaker_builder import TwinMakerRoot, TwinMakerObject

"""Domain Model for the WindFarm sample.
This should allow to read YAML file like this:

Example
-------
        name: ACME WindFarm
        items:
        - name: group1
        type: TurbineGroup
        items:
        - name: turbine_rect_1
            type: Turbine
            device_code: "0x01"
        - name: turbine_rect_2
            type: Turbine
            device_code: "0x02"
        - name: group2
        type: TurbineGroup
        model:
            position: {x: 10, y: 0, z: 0}
        items:
        - name: turbine3
            type: Turbine
            device_code: "0x03"
        - name: turbine4
            type: Turbine
            device_code: "0x04"
        - name: turbine5
            type: Turbine
            device_code: "0x05"
"""


class WindFarm(TwinMakerRoot):
    pass


class TurbineGroup(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(
            description, parent=parent, fields=["shape", "width", "diameter"]
        )


class Turbine(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent, fields=["device_code"])
