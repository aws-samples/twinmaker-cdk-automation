# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iottwinmaker as twinmaker,
    aws_iam as iam,
    RemovalPolicy,
)

from constructs import Construct
from os import path, makedirs


from wind_farm.wind_farm import WindFarm, TwinMakerRoot
from wind_farm.visitors import WindFarmCDKVisitor, WindFarmSceneVisitor
from .random_component import RandomTwinMakerComponent


class WindFarmStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Save account and region for later use
        account = Stack.of(self).account
        region = Stack.of(self).region

        workspace_id = "windfarm-sample"

        # 1. Create an S3 bucket for the TwinMaker Workspace
        bucket_name = f"twinmaker-windfarm-{account}-{region}"
        twinmaker_bucket = s3.Bucket(
            self,
            "TwinMakerResources",
            bucket_name=bucket_name,
            # Block every public access
            access_control=s3.BucketAccessControl.PRIVATE,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            # Encrypt Data at rest
            encryption=s3.BucketEncryption.S3_MANAGED,
            # Encrypt Data in transit
            enforce_ssl=True,
            # Enable versioning
            versioned=True,
            ## Retain S3 bucket
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            # https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html
            object_ownership=s3.ObjectOwnership.OBJECT_WRITER,
        )

        # 2. Create a role to be used by the TwinMaker Workspace
        lambda_name = RandomTwinMakerComponent.lambda_name()
        twinmaker_role = iam.Role(
            self,
            "TwinMakerRoleForS3",
            role_name="windfarm-sample-twinmaker-role",
            assumed_by=iam.ServicePrincipal("iottwinmaker.amazonaws.com"),
            inline_policies={
                "s3_access": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "s3:ListBucket",
                                "s3:GetBucket*",
                                "s3:GetObject",
                                "s3:PutObject",
                            ],
                            resources=[
                                twinmaker_bucket.bucket_arn,
                                f"{twinmaker_bucket.bucket_arn}/*",
                            ],
                            effect=iam.Effect.ALLOW,
                        ),
                        iam.PolicyStatement(
                            actions=["s3:DeleteObject"],
                            resources=[
                                f"{twinmaker_bucket.bucket_arn}/DO_NOT_DELETE_WORKSPACE_{workspace_id}"
                            ],
                            effect=iam.Effect.ALLOW,
                        ),
                        iam.PolicyStatement(
                            actions=["lambda:invokeFunction"],
                            resources=[
                                f"arn:aws:lambda:{region}:{account}:function:{lambda_name}"
                            ],
                            effect=iam.Effect.ALLOW,
                        ),
                    ]
                )
            },
        )

        # 3. Create the Workspace
        workspace = twinmaker.CfnWorkspace(
            self,
            "TwinMakerWorkspace",
            workspace_id="windfarm-sample",
            role=twinmaker_role.role_arn,
            s3_location=twinmaker_bucket.bucket_arn,
        )
        workspace.node.add_dependency(twinmaker_role)
        workspace.node.add_dependency(twinmaker_bucket)

        # 4. Create our custom Random Component
        random_component = RandomTwinMakerComponent(
            self, "RandomComponent", workspace.workspace_id
        )
        random_component.node.add_dependency(workspace)

        # 5. Read the business model
        farm = TwinMakerRoot.load_from_yaml("wind_farm/farm.yaml", WindFarm)

        # 6. Visit the model with the CDKVisitor
        visitor = WindFarmCDKVisitor(self, "WindFarm", workspace)
        farm.visit(visitor)
        visitor.node.add_dependency(random_component)

        # 7. Visit the model wiht the SceneVisitor
        visitor = WindFarmSceneVisitor(bucket_name, "wind_farm/base.json")
        farm.visit(visitor)

        # 8. Upload the scene JSON to the S3 Bucket
        deploy = s3deploy.BucketDeployment(
            self,
            "DeployTwinMakerModels",
            sources=[
                s3deploy.Source.asset("twinmaker_resources"),
                s3deploy.Source.data("scene/windfarm.json", visitor.get_content()),
            ],
            destination_bucket=twinmaker_bucket,
            prune=False,
        )

        # 9. Create the scene in the TwinMaker Workspace
        scene = twinmaker.CfnScene(
            self,
            "MainScene",
            scene_id="windfarm",
            workspace_id=workspace_id,
            content_location=twinmaker_bucket.s3_url_for_object("scene/windfarm.json"),
        )

        scene.node.add_dependency(deploy)
