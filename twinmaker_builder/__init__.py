# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from typing import Mapping
from aws_cdk import aws_iottwinmaker as twinmaker

from os import path
import sys
import inspect
import yaml
from constructs import Construct
import json
import re
import logging

from ngsildclient.utils.urn import Urn

from .scene import SceneNode, JSONEncoder

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class TwinMakerObject:
    def __init__(self, description: dict, parent=None, fields=None) -> None:
        self.items = []
        self.parent = parent

        self.model = description["model"] if "model" in description else None
        self._name = description["name"] if "name" in description else None
        self._id = description["id"] if "id" in description else None

        if fields:
            self.read_props(description, fields)

    def visit(self, visitor):
        visitor.accept(self)

        for item in self.items:
            item.visit(visitor)

    def read_props(self, description: dict, fields):
        for field in fields:
            self.__dict__[field] = description[field] if field in description else None

    @property
    def index(self):
        return self.parent.items.index(self) if self.parent else 0

    @property
    def urn(self):
        if self._id:
            final_id = self._id
        else:
            final_id = self.infer_id_from_name()

        return Urn(nss=f"{type(self).__name__}:{final_id}")

    def infer_id_from_name(self):
        return self.name.replace(" ", "")

    @property
    def name(self):
        return self._name


class TwinMakerRoot(TwinMakerObject):
    def __init__(self, description: dict) -> None:
        super().__init__(description)
        self._description = description

        self.klasses = {}
        for name, obj in inspect.getmembers(sys.modules[self.__module__]):
            if inspect.isclass(obj):
                self.klasses[name] = obj

        if "items" in description:
            for item in description["items"]:
                try:
                    self.items.append(self.build_item(item, self))
                except Exception as e:
                    LOGGER.info("Unable to build item: " + str(e))

    def build_item(self, item_description: dict, parent=None) -> TwinMakerObject:
        if "type" not in item_description:
            raise Exception("No type defined for item")

        type = item_description["type"]
        item = None

        if type in self.klasses:
            item = self.klasses[type](item_description, parent=parent)

        if item and "items" in item_description:
            for sub_item in item_description["items"]:
                item.items.append(self.build_item(sub_item, parent=item))

        if item:
            return item
        else:
            raise Exception(f"Item type not found : {type}")

    def load_from_yaml(description_file_path: str, klass):
        if not path.exists(description_file_path):
            raise Exception(
                f"Path for site description not found: {description_file_path}"
            )

        with open(description_file_path) as file:
            description = yaml.load(file, Loader=yaml.FullLoader)
            return klass(description)


class TwinMakerCDKVisitor(Construct):
    def __init__(
        self, scope: "Construct", id: str, workspace: twinmaker.CfnWorkspace
    ) -> None:
        super().__init__(scope, id)

        self._workspace = workspace
        self._index_entities: Mapping[str, twinmaker.CfnEntity] = {}

        self.node.add_dependency(workspace)

    def to_snake_case(name):
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        name = re.sub("__([A-Z])", r"_\1", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return name.lower()

    def accept(self, entity: TwinMakerObject):
        klass = type(entity).__name__
        method_name = f"on_{TwinMakerCDKVisitor.to_snake_case(klass)}"
        method = getattr(self, method_name, None)
        if callable(method):
            twinmaker_entity = method(entity)

            # Index entities by their entity_id to be able to reference them when
            # creating the dependency
            self._index_entities[twinmaker_entity.entity_id] = twinmaker_entity

            # If entity has a parent, add the dependency
            if twinmaker_entity.parent_entity_id:
                parent = self._index_entities[twinmaker_entity.parent_entity_id]
                twinmaker_entity.node.add_dependency(parent)


class SceneVisitor:
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
        method_name = f"on_{TwinMakerCDKVisitor.to_snake_case(klass)}"
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

    def get_entity_path(self, entity: TwinMakerObject) -> str:
        """Return the path of of an entity in the hierarchy"""
        if entity.parent:
            return self.get_entity_path(entity.parent) + "/" + entity.name
        else:
            return entity.name
