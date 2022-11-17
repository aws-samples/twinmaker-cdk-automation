# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import aws_iottwinmaker as twinmaker

from twinmaker_builder.scene import SceneNode, SceneCoord, ModelShader
from twinmaker_builder import TwinMakerCDKVisitor, SceneVisitor

from .wind_farm import WindFarm
from .random_component import RandomTwinMakerComponent


class WindFarmCDKVisitor(TwinMakerCDKVisitor):
    pass


class WindFarmSceneVisitor(SceneVisitor):
    pass
