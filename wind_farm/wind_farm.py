# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

import yaml
from os import path

from ngsildclient.utils.urn import Urn


class TwinMakerObject:
    def __init__(self, description: dict, parent=None) -> None:
        self.items = []
        self.parent = parent
        self.model = None

        self._name = description["name"] if "name" in description else None
        self._id = description["id"] if "id" in description else None

    def visit(self, visitor):
        visitor.accept(self)

        for item in self.items:
            visitor.accept(item)

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

        if "items" in description:
            for item in description["items"]:
                self.items.append(self.build_item(item, self))

    def build_item(self, item_description: dict, parent=None) -> TwinMakerObject:
        if "type" not in item_description:
            raise Exception("No type defined for item")

        type = item_description["type"]
        item = None

        if type in globals():
            klass = globals()[type]
            item = klass(item_description, parent=parent)

        if "items" in item_description:
            for sub_item in item_description["items"]:
                item.items.append(self.build_item(sub_item, parent=item))

        if item:
            return item
        else:
            raise Exception("Item type not found")

    def load_from_yaml(description_file_path: str, klass):
        if not path.exists(description_file_path):
            raise Exception(
                f"Path for site description not found: {description_file_path}"
            )

        with open(description_file_path) as file:
            description = yaml.load(file, Loader=yaml.FullLoader)
            return klass(description)


class WindFarm(TwinMakerRoot):
    pass


class TurbineGroup(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent)

        self.shape = description["shape"] if "shape" in description else None
        self.width = description["width"] if "width" in description else None
        self.diameter = description["diameter"] if "diameter" in description else None


class Turbine(TwinMakerObject):
    def __init__(self, description: dict, parent=None) -> None:
        super().__init__(description, parent=parent)

        self.device_code = (
            description["device_code"] if "device_code" in description else None
        )
