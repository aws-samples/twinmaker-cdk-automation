# Twinmaker Builder with CDK

This sample project shows a pattern on how to dynamically create entities in Twinmaker
and generate the corresponding 3D scene by using CDK automation.

## Introduction

When using TwinMaker and generating digital twins of real objects, it can quickly become
overwhelming defining all the automation to generate a complex scene. Most of the time, you 
can find repeated objects in the scene that share the same properties or repeatable patterns. 
For instance, in a warehouse, you can find multiple `gates` on a `dock`. They share the same type and often the
same appearance. There is no real need to define all of them each time.

Simplifying the definition of a digital twin will allow scaling vertically (building bigger twins) and
horizontally (building lots of twins).

The idea is to simplify the definition of the digital twin and use some business vocabulary 
(called domain model) to describe it. Our code will then visit that model and transform it
in two different ways :

 - the hierarchy of TwinMaker entities
 - the 3D scene for TwinMaker

In this sample, we will build a wind farm composed of wind turbines that are place following
shapes on a field : 

<img src="./doc/windfarm.png"/>

## Domain Model

The Domain Model is your model, and you can define whatever you want in it : has nothing to do with AWS or AWS IoT Twinmaker. 
In this sample, we will have several objects:

 - `WindFarm` : It is the root object and we can define some parametter like a name for instance
 - `TurbineGroup` : It is a group of wind turbines that defines how wind turbine are spread. It also defines a position.
 - `Turbine` : It defines a turbine and its properties, especially a identifier that allows us to identify the data to fetch

We are then able to define our WindFarm with a YAML file like this:

```yaml
name: ACME WindFarm
items:
- name: group1
  type: TurbineGroup  
  items:
  - name: turbine_rect_1
    type: Turbine
    device_code: "0x01"
  - name: turbine_rect_2
    type: Turbine
    device_code: "0x02"
- name: group2
  type: TurbineGroup
  model:    
    position: {x: 10, y: 0, z: 0}
  items:
  - name: turbine3
    type: Turbine
    device_code: "0x03"
  - name: turbine4
    type: Turbine
    device_code: "0x04"
  - name: turbine5
    type: Turbine
    device_code: "0x05"
  

  ...
```

This definition file doesn't mention any AWS construction and anybody who can read YAML will be able to understand and make changes to it.

## What's included ?

### Complete CDK Twinmaker Deployment

This is a regular CDK repository, so running the following recipe :

```
$ python3 -m venv .venv
$ . ./.venv/bin/activate
$ pip install -r requirements.txt
$ cdk deploy
```

will deploy the complete TwinMaker project.

### A Domain Model Reader

The `twinmaker_builder` module contains objects that allow to read the YAML file and dynamically link it to existing class implementation. For instance, the following code allows to load the domain model:

```python
farm = TwinMakerRoot.load_from_yaml("wind_farm/farm.yaml", WindFarm)
```

### Two Visitor Base Classes

Once the domain model is loaded, we can visit its entities. Two base abstract classes are provided:

 - `TwinMakerCDKVisitor` : visits the model to generate some calls to CDK. 
 - `SceneVisitor` : visits the model to generate a Twinmaker 3D scene in JSON. 

Concrete classes implementing those class have to implement hooks methods like `on_turbine` that are dynamically introspected and called by the visiting mechanism. More on how to create your own model and visiting mechanism can be found in the [start from scratch documentation](doc/start_from_scratch.md)


### A Random Component Type

The `random_component` module contains the implementation of a TwinMaker component type that return random values. It is helpful to stub datasources.


### Tests

Unit tests are provided to verify everything is still working. It is a great source to understand how everything work.


