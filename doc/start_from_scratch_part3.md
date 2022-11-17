# Start Building Digital Twin From Scratch Part 3

## Start From Here

In order to start directly from here, you can run the following command :

```shell
git checkout from-scratch-part3
```

## Generating A TwinMaker 3D scene

Even if we can simply [create a TwinMaker scene with CDK](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iottwinmaker/CfnScene.html), the description of that scene is made with a JSON file held in the S3 bucket of the TwinMaker bucket. The idea is to generate the this JSON file by visiting our 3D model. The `twinmaker_library` provides a `SceneVisitor` abstract object that we can inherit from. That visitor takes care of several things:
- it start from a base JSON file that can include all the Twinmaker rules or global settings
- it infers from the type of the visited entity the name of the hook to call. For instance, if the visited entity is of type `Turbine`, it will check for a `on_turbine` hook and call it.
- it handles the hierarchy of entities and recreates it in the JSON file.
- when the object has a non empyt `model` property, is uses it to define the URI of the model and all the transformations (position, scale and rotation)

The JSON file is started with a `base.json` bootstrap file that contains an empty `nodes` property. The visitor will populate that property with nodes like this:

```json
{
  "name": "turbine_2",
  "transform": {
    "position": [0,0,10],
    "rotation": [0,0,0],
    "scale": [1,1,1]
  },
  "transformConstraint": {},
  "children": [],
  "components": [
    {
      "type": "ModelRef",
      "uri": "s3://twinmaker-windfarm-039665761580-eu-west-1/models/animated_wind_turbine.glb",
      "modelType": "GLB",
      "unitOfMeasure": "millimeters",
      "castShadow": true,
      "receiveShadow": true
    },
    {
      "type": "ModelShader",
      "valueDataBinding": {
        "dataBindingContext": {
          "entityId": "urn:ngsi-ld:Turbine:turbine_2",
          "componentName": "TurbineFan",
          "propertyName": "speed",
          "entityPath": "ACME WindFarm/group1/turbine_2"
        },
        "dataFrameLabel": ""
      },
      "ruleBasedMapId": "turbineColorRule"
    }
  ],
  "properties": {}
}
```

The `SceneVisitor` will ease the creation of such node by using the same hook mechanism. The [test_scene_visitor.py](../tests/unit/test_scene_visitor.py) test bootstraps the scene based on `farm.yaml` to be able to run some tests.

```python
def test_turbine(scene):
    turbine = scene["nodes"][2]
    assert turbine["name"] == "turbine_rect_1"

    assert "transform" in turbine
    assert "position" in turbine["transform"]
    assert "rotation" in turbine["transform"]
    assert "scale" in turbine["transform"]
    assert turbine["transform"]["position"] == [0, 0, 0]
    assert turbine["transform"]["rotation"] == [0, 0, 0]
    assert turbine["transform"]["scale"] == [1, 1, 1]

    assert "components" in turbine
    assert len(turbine["components"]) == 2
    assert (
        turbine["components"][0]["uri"]
        == "s3://test_bucket/models/animated_wind_turbine.glb"
    )

    assert len(turbine["children"]) == 0
```

To make that test pass, we need to implent the `on_turbine` hook in the `WindFarmSceneVisitor` object:

```python
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
```

The interesting part about that hook is that it is passed the visited entity and a `SceneNode` that we can modify.
There is potentially no limit to what can be done here.

`WindFarm` and `TurbineGroup` are just containers, so we don't need to add any specific hooks.

The two `TurbineGroup`s are positionned at the same spot. In order to shift one from another, we can edit the `farm.yaml` file and specify the group position by setting a `model` property:

```yaml
- name: group2
  type: TurbineGroup
  model:
    position: {x: 10, y: 0, z: 0}
  items:
  - name: turbine3
    type: Turbine
...
```
The other properties that can be defined here are:
- `scale`: define the scale of the imported model
- `rotation`: defines the rotation of the entity
- `uri`: defines the location of the 3D model to be used. It is relative to the root of the workspace's S3 bucket.

## What's next
 - [Part 4 : Assembling the CDK stack](./start_from_scratch_part4.md)

