# Start Building Digital Twin From Scratch Part 0

## Starting From Scratch With Git

This repository has a special branch name `from-scratch`. It contains all the reusable code and all the bootstrap files to start building a digital twin but without the real windfarm code. Following this guide will allow us to build those specific files. In order to switch to that branch, you can run the following code :

```shell
$ git checkout from-scratch
```

You can verify that all went well by looking at the content of `tests/unit/farm.yaml` that should only contain the following :

```yaml
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

name: ACME WindFarm
```

## Starting From A Specific Step

If you want to start from a specific part, some Git tags have been placed to start from there. For instance, to start from part 3, you can run the following command :

```shell
git checkout from-scratch-part3
```

## What's next
 - [Part 1 : Creating the domain model](./start_from_scratch_part1.md)
 - [Part 2 : Visiting the model with CDK](./start_from_scratch_part2.md)
 - [Part 3 : Visiting the model to generate a 3D scene](./start_from_scratch_part3.md)
 - [Part 4 : Assembling the CDK stack](./start_from_scratch_part4.md)

 


