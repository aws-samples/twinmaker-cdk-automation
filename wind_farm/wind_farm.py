# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0


from scale_twinmaker import TwinMakerRoot, TwinMakerObject


class WindFarm(TwinMakerRoot):
    pass


class TurbineGroup(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent)
        self.read_props(description, ["shape", "width", "diameter"])


class Turbine(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent)
        self.read_props(description, ["device_code"])
