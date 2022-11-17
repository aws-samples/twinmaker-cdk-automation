# Start Building Digital Twin From Scratch Part 2

## Start From Here

In order to start directly from here, you can run the following command :

```shell
git checkout from-scratch-part2
```

## Generating TwinMaker Entities With CDK

Now that we have a domain model to describe our windfarm, we will use a [visitor pattern](https://en.wikipedia.org/wiki/Visitor_pattern) to visit that model in order to generate some [TwinMaker entities](https://docs.aws.amazon.com/iot-twinmaker/latest/guide/twinmaker-gs-entity.html).

The `twinmaker_builder` module provide a base abstract visitor `TwinMakerCDKVisitor` that we will extend. That visitor provides several features:

- it infers from the type of the visited entity the name of the hook to call. For instance, if the visited entity is of type `Turbine`, it will check for a `on_turbine` hook and call it.
- it handles the dependency between the various entity

Inside a CDK construct, it can be used like this:

```python
farm = TwinMakerRoot.load_from_yaml(filename, WindFarm)
visitor = WindFarmCDKVisitor(self, "WindFarm", self.workspace)
```

### Generating The Root Entity

The [test_cdk_visitor.py](../test/unit/test_cdk_visitor.py) test bootstraps a dummy stack based on `farm.yaml` that allows us to test the generation of the entity. CDK generates a [CloudFormation](https://aws.amazon.com/cloudformation/) template that we can test like this:

```python
def test_root(stack):
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::IoTTwinMaker::Entity",
        {
            "EntityName": "ACME WindFarm",
            "EntityId": "urn:ngsi-ld:WindFarm:ACMEWindFarm",
            "Components": {},
        },
    )
```

To make that test pass, we need to add a hook in the visitor. The name of the hook is based on the [snake_case](https://en.wikipedia.org/wiki/Snake_case) conversion of the object type. For instance:

| Object Type  | Snake case conversion | hook name        |
| ------------ | --------------------- | ---------------- |
| WindFarm     | wind_farm             | on_wind_farm     |
| TurbineGroup | turbine_group         | on_turbine_group |
| Turbine      | turbine               | on_turbine       |

For the `WindFarm` object this will give:



```python
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
```
When the model is visited, for every `WindFarm`, this will called  the [CfnEntity](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iottwinmaker/CfnEntity.html) CDK construct. The visitor (`self`) is also a CDK construct that has a reference on the workspace. Having the domain object also allows to use some of its property like the URN or the name.

We can repeat this operation for the two others object. For the `Turbine` object though, we need to add a component to capture the speed. It will use the `RandomComponent` type that generates random data between a min and a max:

```python
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
```

After visiting the model, we've been able to generate some CDK calls to deploy TwinMaker entities.

## What's next
 - [Part 3 : Visiting the model to generate a 3D scene](./start_from_scratch_part3.md)
 - [Part 4 : Assembling the CDK stack](./start_from_scratch_part4.md)

 


