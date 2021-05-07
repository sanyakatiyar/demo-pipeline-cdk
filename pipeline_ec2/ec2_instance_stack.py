import os.path
from aws_cdk.core import App, Stack, Environment
from aws_cdk.aws_s3_assets import Asset
 
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core    
)

from aws_cdk.core import Tags
 
# __filepath__ = '/Documents/escoe/ccf-infra/configuration.sh'
# __filepath__ = '/Users/sk27784/ec2_demo/ec2_demo/config.sh'
# dirname = os.path.dirname(__filepath__)
 
class EC2InstanceStack(core.Stack):
 
    def __init__(self, scope: core.Construct, id: str, ec2_role : iam.Role, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
 
        ## VPC of the instance
 
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)
                ]
            )
        sg = ec2.SecurityGroup(self, id="sg", vpc=vpc)

        sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(),
                            connection=ec2.Port.tcp(80))

        sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(),
                            connection=ec2.Port.tcp(22))
        # vpc = ec2.Vpc(self, "VPC", cidr="172.32.0.0/16",max_azs=3,enable_dns_hostnames=True, enable_dns_support=True,
        #                 subnet_configuration=[
        #                     ec2.SubnetConfiguration(name="Public",subnet_type=ec2.SubnetType.PUBLIC,cidr_mask=24),
        #                     ec2.SubnetConfiguration(name="Private",subnet_type=ec2.SubnetType.PRIVATE,cidr_mask=24)
        #                 ]
        # )
 
        ##AMI 
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
                    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                    edition=ec2.AmazonLinuxEdition.STANDARD,
                    virtualization=ec2.AmazonLinuxVirt.HVM,
                    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
 
        # Instance Role and SSM Managed Policy
        # role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
 
        # role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))
 
        # Instance
        
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amzn_linux,
            vpc = vpc,
            role = ec2_role, 
            security_group=sg
            )

        # f = open("C:\\Users\\sk27784\\Documents\\pipeline-ec2-demo\\pipeline_ec2_demo\\config.sh")
        # instance.add_user_data(f.read())
        # instance.user_data.add_execute_file_command(file_path = "/ec2_demo/ec2_demo/config.sh")
        # userData = instance.user_data.add_commands('sudo yum install python35-pip', 'sudo yum install python35')
        # userData.addCommands('sudo yum install python35-pip')
        # userData.addCommands('sudo yum install python35')
 
        # instance.add_user_data('sudo yum install python35', 'sudo yum install python35-pip')
        # instance.add_user_data('sudo yum install python35-pip')

        instance.add_user_data("sudo yum install httpd -y")
        instance.add_user_data("sudo systemctl start httpd")
        instance.add_user_data("sudo systemctl enable httpd")
        instance.add_user_data("sudo echo '<h1> this is cdk instance! hello hi</h1>' >> /var/www/html/index.html")

        Tags.of(instance).add("Owner", "sanya")

 
# app = core.App()
# EC2InstanceStack(app, "ec2-instance")
 
# app.synth()