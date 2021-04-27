from aws_cdk import core 

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_ssm as ssm,
    aws_secretsmanager as sm,
    aws_iam as iam,
)
import os
import json

 
class IAMStack(core.Stack):

    # role_ec2 : iam.Role
 
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.role_ec2 = iam.Role(self, "ec2-instance-role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"), 
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEMRFullAccessPolicy_v2"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSESFullAccess"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSReadOnlyAccess"),
                                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSFullAccess")
                                ]
        )
        # role_emr = iam.Role(self, "emr-instance-role", assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com"))
        # role_rds = iam.Role(self, "rds-role", assumed_by=iam.ServicePrincipal("rds.amazonaws.com"),
        #                 managed_policies=[
        #                         iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSServiceRolePolicy")
        #                         ]
        # )

        self.role_emr = iam.Role(self, "emr-instance-role", assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonElasticMapreduceRole"),
                            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
                        ]
        )

        self.role_emr_ec2 = iam.Role(self, "emr-ec2-instance-role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonElasticMapReduceforEC2Role")
                        ]
        )
