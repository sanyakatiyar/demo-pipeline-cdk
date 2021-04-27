#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from pipeline_ec2.pipeline_ec2_stack import PipelineEc2Stack
from pipeline_ec2.ec2_instance_stack import EC2InstanceStack
from pipeline_ec2.iam_stack import IAMStack


app = core.App()
roles = IAMStack(app, "IAMroleEC2", env={'account' : '189186734332','region' : 'ap-south-1'})
EC2InstanceStack(app, "ec2Instance2", env={'account' : '189186734332','region' : 'ap-south-1'}, ec2_role = roles.role_ec2)
PipelineEc2Stack(app, "PipelineEc2Stack", env={'account' : '189186734332','region' : 'ap-south-1'})

app.synth()

