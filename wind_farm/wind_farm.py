# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0


from twinmaker_builder import TwinMakerRoot, TwinMakerObject


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
