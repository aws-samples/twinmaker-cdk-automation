# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from typing import Mapping
from aws_cdk import aws_iottwinmaker as twinmaker

from .wind_farm import TwinMakerObject, WindFarm, TurbineGroup, Turbine
from .scene import SceneNode, JSONEncoder

from constructs import Construct
import json
import re


class TwinMakerCDKVisitor(Construct):
    def __init__(
        self, scope: "Construct", id: str, workspace: twinmaker.CfnWorkspace
    ) -> None:
        super().__init__(scope, id)

        self._workspace = workspace
        self._index_entities: Mapping[str, twinmaker.CfnEntity] = {}

    def accept(self, entity: TwinMakerObject):
        pass


class WindFarmCDKVisitor(TwinMakerCDKVisitor):
    def to_snake_case(name):
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        name = re.sub("__([A-Z])", r"_\1", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return name.lower()

    def accept(self, entity: TwinMakerObject):
        klass = type(entity).__name__
        method_name = f"on_{WindFarmCDKVisitor.to_snake_case(klass)}"
        method = getattr(self, method_name, None)
        if callable(method):
            method(entity)

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


class WindFarmSceneVisitor:
    def __init__(self, s3_bucket_name, base_file: str = "base.json") -> None:

        self.s3_bucket_name = s3_bucket_name

        # Initialize content JSON
        with open(base_file) as file:
            self.content = json.load(file)

        # entity_id to entity
        self.entity_index = {}

    def add_node(self, node: SceneNode):
        self.content["nodes"].append(node)

    def accept(self, entity: TwinMakerObject):
        node = SceneNode(self, entity.name, model=entity.model)
        self.entity_index[entity.urn.fqn] = (entity, node)
        self.add_node(node)

        klass = type(entity).__name__
        method_name = f"on_{WindFarmCDKVisitor.to_snake_case(klass)}"
        method = getattr(self, method_name, None)
        if callable(method):
            method(entity, node)

        # To handle hierarchy of nodes
        entity_index = self.content["nodes"].index(node)
        if entity.parent:
            parent_node = self.entity_index[entity.parent.urn.fqn][1]
            parent_node.children.append(entity_index)
            print(len(parent_node.children))
        else:
            self.content["rootNodeIndexes"].append(entity_index)

    def get_content(self):
        return JSONEncoder().encode(self.content)

    def on_wind_farm(self, farm: WindFarm, node: SceneNode):
        pass

    def on_turbine_group(self, group: TurbineGroup, node: SceneNode):
        pass

    def on_wind_turbine(self, turbine: Turbine, node: SceneNode):
        pass
