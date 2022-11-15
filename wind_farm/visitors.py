# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import aws_iottwinmaker as twinmaker

from twinmaker_builder.scene import SceneNode
from twinmaker_builder import TwinMakerCDKVisitor, SceneVisitor

from .wind_farm import WindFarm, TurbineGroup, Turbine


class WindFarmCDKVisitor(TwinMakerCDKVisitor):
    def on_wind_farm(self, farm: WindFarm):
        return twinmaker.CfnEntity(
            self,
            f"WindFarm{farm.name}",
            parent_entity_id=farm.parent.urn.fqn if farm.parent else None,
            entity_name=farm.name,
            entity_id=farm.urn.fqn,
            workspace_id=self._workspace.workspace_id,
            components={},
        )

    def on_turbine_group(self, group: TurbineGroup):
        return twinmaker.CfnEntity(
            self,
            f"TurbineGroup{group.name}",
            parent_entity_id=group.parent.urn.fqn if group.parent else None,
            entity_name=group.name,
            entity_id=group.urn.fqn,
            workspace_id=self._workspace.workspace_id,
            components={},
        )

    def on_turbine(self, turbine: Turbine):
        return twinmaker.CfnEntity(
            self,
            f"Turbine{turbine.name}",
            parent_entity_id=turbine.parent.urn.fqn if turbine.parent else None,
            entity_name=turbine.name,
            entity_id=turbine.urn.fqn,
            workspace_id=self._workspace.workspace_id,
            components={},
        )


class WindFarmSceneVisitor(SceneVisitor):
    def on_wind_farm(self, farm: WindFarm, node: SceneNode):
        pass

    def on_turbine_group(self, group: TurbineGroup, node: SceneNode):
        pass

    def on_wind_turbine(self, turbine: Turbine, node: SceneNode):
        pass
