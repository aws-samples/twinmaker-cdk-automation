# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from typing import Mapping
from aws_cdk import aws_iottwinmaker as twinmaker

from .wind_farm import *
from .scene import *

from constructs import Construct
import json


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
    def accept(self, entity: TwinMakerObject):
        if WindFarm == type(entity):
            self.on_wind_farm(entity)

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
    
        if WindFarm == type(entity):
            self.on_wind_farm(entity)

    def get_content(self):
        return JSONEncoder().encode(self.content)

    def on_wind_farm(self, farm: WindFarm):
        pass

    