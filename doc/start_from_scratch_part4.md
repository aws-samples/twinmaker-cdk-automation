# Start Building Digital Twin From Scratch Part 4

## Start From Here

In order to start directly from here, you can run the following command :

```shell
git checkout from-scratch-part4
```

## Assembling the full stack

The last part of this guide is to assemble everything that we saw in a nice CDK construction. The different parts are as follow:

 1. Create an S3 bucket for the TwinMaker Workspace
 2. Create a role to be used by the TwinMaker Workspace
 3. Create the Workspace
 4. Create our custom Random Component
 5. Read the business model
 6. Visit the model with the CDKVisitor
 7. Visit the model wiht the SceneVisitor
 8. Upload the scene JSON to the S3 Bucket
 9. Create the scene in the TwinMaker Workspace

The resulting script can be found in [wind_farm_stack.py](../wind_farm/wind_farm_stack.py) and the steps are outlined in the comments.

It's now time to deploy:

```shell
% cdk deploy
```

## What's next
 - Let's go build your own models and share you results!

