# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

import json


# extend the json.JSONEncoder class
class JSONEncoder(json.JSONEncoder):
    # overload method default
    def default(self, obj):
        if isinstance(obj, SceneCoord):
            return [obj.x, obj.y, obj.z]
        return obj.__dict__


class SceneCoord:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def from_dict(position):
        return SceneCoord(x=position["x"], y=position["y"], z=position["z"])


class SceneTransform:
    position: SceneCoord
    rotation: SceneCoord
    scale: SceneCoord

    @staticmethod
    def DEFAULT():
        st = SceneTransform()
        st.position = SceneCoord()
        st.rotation = SceneCoord()
        st.scale = SceneCoord(1, 1, 1)
        return st


class SceneNode:
    def __init__(self, parent, name: str, model=None) -> None:
        self.name = name
        self.transform = SceneTransform.DEFAULT()
        self.transformConstraint = {}
        self.children = []
        self.components = []
        self.properties = {}

        if model:
            if "uri" in model:
                uri = model["uri"]
                self.components.append(
                    {
                        "type": "ModelRef",
                        "uri": f"s3://{parent.s3_bucket_name}/{uri}",
                        "modelType": "GLB",
                    }
                )

            if "position" in model:
                self.transform.position = SceneCoord.from_dict(model["position"])

            if "rotation" in model:
                self.transform.rotation = SceneCoord.from_dict(model["rotation"])

            if "scale" in model:
                self.transform.scale = SceneCoord.from_dict(model["scale"])


class ModelShader:
    def __init__(
        self,
        entity_id: str,
        component_name: str,
        property_name: str,
        entity_path: str,
        data_frame_label: str,
        rule: str,
    ) -> None:
        self.type = "ModelShader"
        self.valueDataBinding = {
            "dataBindingContext": {
                "entityId": entity_id,
                "componentName": component_name,
                "propertyName": property_name,
                "entityPath": entity_path,
            },
            # TODO: Find a doc to generate that ....
            "dataFrameLabel": data_frame_label,
        }

        self.ruleBasedMapId = rule
