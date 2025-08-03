from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct


class EarningSpyS3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        bucket = s3.Bucket(self, "qa-EarningSpyBucket",
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            auto_delete_objects=False
        )
        # El rol tambien tiene que tener permisos para ser usado localmente desde una notebook
        provider = iam.OpenIdConnectProvider.from_open_id_connect_provider_arn(
            self,
            "qa-GithubOIDCProvider",
            f"arn:aws:iam::{self.account}:oidc-provider/token.actions.githubusercontent.com"
        )
        
        principals = iam.CompositePrincipal(
            
            iam.OpenIdConnectPrincipal(provider).with_conditions({
                "StringEquals": {
                    "token.actions.githubusercontent.com:sub": "repo:c4road/earningspy-platform:*"
                }
            }),
            iam.ArnPrincipal(f"arn:aws:iam::{self.account}:role/QA-DeveloperRole")
        )
        uploader_role = iam.Role(self, "qa-EarningspyDataLoaderRole",
            assumed_by=principals,
            description="Role that can upload/download to the QA data bucket"
        )
        bucket.grant_read_write(uploader_role)

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
