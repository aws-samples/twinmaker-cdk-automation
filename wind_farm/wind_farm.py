# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0


from twinmaker_builder import TwinMakerRoot, TwinMakerObject


class WindFarm(TwinMakerRoot):
    def __init__(self, description: dict) -> None:
        super().__init__(description, fields=["city"])


class TurbineGroup(TwinMakerObject):
    pass


class Turbine(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent, fields=["device_code"])
