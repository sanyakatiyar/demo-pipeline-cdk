from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import(
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpactions,
    aws_codebuild as cb
)

class PipelineEc2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = cp.Artifact()
        build_artifact = cp.Artifact()

        source_action = cpactions.GitHubSourceAction(
            action_name = 'GitHub',
            output = source_artifact,
            oauth_token= core.SecretValue.secrets_manager('github_token'),
            owner = 'sanya-katiyar',
            repo = 'pipeline-ec2',
            trigger = cpactions.GitHubTrigger.WEBHOOK
        )

        build_project = cb.PipelineProject(self, "code_build_2",
                            build_spec=cb.BuildSpec.from_object(
                                dict(
                                    version="0.2",
                                    phases=dict(
                                        install=dict(
                                            commands=[
                                                "npm install aws-cdk",
                                                "npm update",
                                                "pip install -r requirements.txt"
                                            ]),
                                        build=dict(commands=[
                                            "npx cdk --version",
                                            "npx cdk synth",
                                            "npx cdk deploy EC2InstanceStack -y --require-approval=never"
                                        ])
                                    ),
                                    artifacts={
                                        "files": ["**/*"],
                                        "enable-symlinks": "yes"
                                    },
                                    environment=dict(buildImage=cb.LinuxBuildImage.STANDARD_2_0))
                            ),
                            project_name= 'ec2-deploy-cdk-2'
        )

        build_action = cpactions.CodeBuildAction(
                            action_name="deploy_ec2_2",
                            project=build_project,
                            input=source_artifact,
                            outputs=[build_artifact]
                        )

        pipeline = cp.Pipeline(
            self,
            id = "demo-pipeline-2",
            pipeline_name="pipelineec2_2",
            stages=[
                cp.StageProps(stage_name="source_stage", actions=[source_action]),
                cp.StageProps(stage_name="build_stage", actions=[build_action])
            ]
        )
        # The code that defines your stack goes here
