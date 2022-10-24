# Twinmaker CDK automation

This sample project shows a pattern on how to dynamically create entities in Twinmaker
and generate the corresponding 3D scene by using automation.

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

```TODO: insert a picture of the wind farm```

## Domain Model

The Domain Model has nothing to do with AWS or AWS IoT Twinmaker. It is your model, and you
can define whatever you want. In this sample, we will have several objects:

 - `WindFarm` : It is the root object and we can define some parametter like a name for instance
 - `TurbineGroup` : It is a group of wind turbines that defines how wind turbine are spread. It also defines a position.
 - `WindTurbine` : It defines a turbine and its properties, especially a identifier that allows us to identify the data to fetch

We are then able to define our WindFarm with a YAML file like this:

```yaml
name: ACME WindFarm
groups:
- name: group1
  shape: rectangle
  width: 2
  position: { x: 0, y: 0 }
  turbines:
  - name: turbine_rect_1
    device_code: 0x01
  - name: turbine_rect_2
    device_code: 0x02
  ...
- name: group2
  shape: circle
  diameter: 10
  position: { x: 0, y: 20 }
  turbines:
  - name: turbine3
    device_code: 0x03
  - name: turbine4
    device_code: 0x04
  - name: turbine5
    device_code: 0x04
  ...
```

This definition file doesn't mention any AWS construction and anybody who can read YAML will be able to understand and make changes to it.

## Visitor Pattern

### CDK Visitor to create entities

### Scene Visitor to create scene


## How to deploy
### Prerequisites

 - Python 3
 - AWS CLI
 - CDK Library : https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html
 - Docker

### SiteWise Demo assets

### Deploy
```
$ python3 -m venv .venv
$ . ./.venv/bin/activate
$ pip install -r requirements.txt
$ cdk deploy
```

