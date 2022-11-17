# Start Building Digital Twin From Scratch

## What is this guide ?

Diving into the code of that repository and trying to understand the various patterns used can be challenging and time consuming. Especially when you don't want to create a WindFarm digital twin, the challenge is to know what code you need to write by yourself and what code you can reuse. The short answer can be : just write the 5 files in the `wind_farm` module :
 - `farm.yaml` : The description of our domain model in YAML
 - `wind_farm.py` : Our domain model implementation in Python
 - `visitors.py` : The two visitors implementation
 - `wind_farm_stack.py` : The final CDK stack
 - `base.json` : The base file for our Twinmaker 3D description that holds all the rules definitions
 - by far the most important, all the associated test files in `tests/unit/` !
and reuse everything else.

This guide will walk through the creation of all those files : 

 - [Part 0 : Starting from the scratch branch](./start_from_scratch_part0.md)
 - [Part 1 : Creating the domain model](./start_from_scratch_part1.md)
 - [Part 2 : Visiting the model with CDK](./start_from_scratch_part2.md)
 - [Part 3 : Visiting the model to generate a 3D scene](./start_from_scratch_part3.md)
 - [Part 4 : Assembling the CDK stack](./start_from_scratch_part4.md)

 


