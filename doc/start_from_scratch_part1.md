# Start Building Digital Twin From Scratch Part 1

## Start From Here

In order to start directly from here, you can run the following command :

```shell
git checkout from-scratch-part1
```

## Domain Model Description

Let's first start by describing the domain model of our digital twin. We want to be able to deploy WindTurbine at scale. The logic is to align all the turbines and be able to group them. Each group can have its own starting position. The end result should look like this :

<img src="./doc/windfarm.png"/>

We have two groups of turbine, one that is composed of 2 turbines and the other with 3.

## Reading The Model From YAML

### Exploring The Domain Test
When looking at the [tests/unit/farm.yaml](../tests/unit/farm.yaml) file, it currently contains pretty much nothing:

```yaml
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

name: ACME WindFarm
```

The [tests/unit/test_domain.py](../tests/unit/test_domain.py) test allow to see how the `twinmaker_builder` library allows one to read a that file :

```python
@pytest.fixture()
def farm():
    return WindFarm.load_from_yaml("tests/unit/farm.yaml", WindFarm)


def test_can_read_farm_file(farm):
    assert farm.name == "ACME WindFarm"
```

The `WindFarm` class is defined in [windfarm/windfarm.py](../windfarm/windfarm.py) and only inherits from `twinmaker_builder.TwinMakerRoot`.

As we can see, the object already has a `name` property that is read from the YAML definition. By default, 3 properties can be read from the file:

 - `name`: the name of the object
 - `id`: a unique ID, that is optional and by default inherited from the name (removing spaces)
 - `model`: a dict allowing to specify some modeling properties (URI of the 3D file, position, scale etc...)


### Adding a Property to WindFarm

The `twinmaker_builder` library allows to load the YAML file and hydrate the domain object for you. You can add some specific properties that may be helpful. For instance, let's add a `city` property to our `WindFarm`.

We first start by adding an assertion to our test:

```python
def test_can_read_farm_file(farm):
    assert farm.name == "ACME WindFarm"
    assert farm.city == "Seattle"
```

In order to make that test pass, we need to change our YAML file:

```yaml
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2022
# SPDX-License-Identifier: Apache-2.0

name: ACME WindFarm
city: Seattle
```
and the definition of the `WindFarm` object:

```python
class WindFarm(TwinMakerRoot):
    def __init__(self, description: dict) -> None:
        super().__init__(description, fields=["city"])
```

The `fields` parameter in the `TwinMakerRoot` constructor allow to specify some data that must be parsed and added to our object.

Our `WindFarm` object also inherits a `urn` property which is a unique resource notation following the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf) specification. For instance we can add the following assertion to our test:

```python
assert farm.urn.fqn == "urn:ngsi-ld:WindFarm:ACMEWindFarm"
```

### Parent / Child Relations

The `twinmaker_builder` library alos allows to parse parent/child relations in the YAML file by using the `items` property. For instance we can add an assertion in our test:

```python
assert len(farm.items) == 2
```

For the test to pass we need 1/ to add the groups to the yaml file and 2/ define a `TurbineGroup` object that inherits from `TwinMakerObject`.

in [tests/unit/farm.yaml](../tests/unit/farm.yaml):

```yaml
name: ACME WindFarm
city: Seattle
items:
- name: group1
  type: TurbineGroup
- name: group2
  type: TurbineGroup
```
and in [/windfarm/windfarm.py](../windfarm/windfarm.py):

```python
class TurbineGroup(TwinMakerObject):
    pass
```

The name of the class has to match the type that is specified in the YAML file. We can also add the following test, to verify the properties of our new `TurbineGroup` object:

```python
def test_farm_has_turbine_groups(farm):
    group = farm.items[0]
    assert type(group) == TurbineGroup
    assert group.urn.fqn == "urn:ngsi-ld:TurbineGroup:group1"

    assert group.parent is not None
    assert group.parent == farm
```

We can see that the `TurbineGroup` also has a `urn` property but also a `parent` property that will allow to browse the entire hierarchy of objects.

The only remaining object that needs to be added is a `Turbine` object with a `device_code` property. There are always 3 steps to do this:
 - write the test
 - add some domain description in the YAML file
 - declare the objects in the `wind_farm.py` file.

The is let as an exercise for the rest of this part. The result can be found on the `from-scratch-part2` tag of the repository.

We now have a hierarchical domain model that allows to describe our digital twins. That model is easily extensible, and the YAML file allows to describe it in business terms. From that domain model, we will now derive to generate the various Twinmaker constructions.

## What's next
 - [Part 2 : Visiting the model with CDK](./start_from_scratch_part2.md)
 - [Part 3 : Visiting the model to generate a 3D scene](./start_from_scratch_part3.md)
 - [Part 4 : Assembling the CDK stack](./start_from_scratch_part4.md)

 


