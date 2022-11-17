# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import aws_iottwinmaker as twinmaker

from twinmaker_builder.scene import SceneNode, SceneCoord, ModelShader
from twinmaker_builder import TwinMakerCDKVisitor, SceneVisitor

from .wind_farm import WindFarm, Turbine, TurbineGroup
from .random_component import RandomTwinMakerComponent


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
            components={
                "TurbineFan": twinmaker.CfnEntity.ComponentProperty(
                    component_type_id=RandomTwinMakerComponent.TYPE,
                    properties={
                        "min": twinmaker.CfnEntity.PropertyProperty(
                            value=twinmaker.CfnEntity.DataValueProperty(double_value=50)
                        ),
                        "max": twinmaker.CfnEntity.PropertyProperty(
                            value=twinmaker.CfnEntity.DataValueProperty(
                                double_value=150
                            )
                        ),
                    },
                )
            },
        )


class WindFarmSceneVisitor(SceneVisitor):
    def on_turbine(self, turbine: Turbine, node: SceneNode):
        # Separating each turbine by 10 meter
        node.transform.position.z = turbine.index * 10

        # Hard coding the 3D model used
        node.components.append(
            {
                "type": "ModelRef",
                "uri": f"s3://{self.s3_bucket_name}/models/animated_wind_turbine.glb",
                "modelType": "GLB",
                "unitOfMeasure": "millimeters",
                "castShadow": True,
                "receiveShadow": True,
            }
        )

        # Linking a shader to the entity data
        node.components.append(
            ModelShader(
                entity_id=turbine.urn.fqn,
                component_name="TurbineFan",
                property_name="speed",
                entity_path=self.get_entity_path(turbine),
                data_frame_label="",
                rule="turbineColorRule",
            ).__dict__
        )
