#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.pathweaver_stack import PathWeaverStack

app = cdk.App()

PathWeaverStack(
    app,
    "PathWeaverStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
    ),
)

app.synth() 