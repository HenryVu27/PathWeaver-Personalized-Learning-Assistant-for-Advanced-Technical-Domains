from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_opensearchservice as opensearch,
    aws_iam as iam,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class PathWeaverStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for storing documents and embeddings
        self.document_bucket = s3.Bucket(
            self,
            "DocumentBucket",
            removal_policy=RemovalPolicy.RETAIN,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # OpenSearch domain for vector search
        self.vector_store = opensearch.Domain(
            self,
            "VectorStore",
            version=opensearch.EngineVersion.OPENSEARCH_2_3,
            capacity=opensearch.CapacityConfig(
                data_node_instance_type="t3.small.search",
                data_nodes=1,
            ),
            ebs=opensearch.EbsOptions(
                volume_size=10,
                volume_type=opensearch.EbsVolumeType.GP3,
            ),
            removal_policy=RemovalPolicy.RETAIN,
        )

        # DynamoDB table for user profiles
        self.user_table = dynamodb.Table(
            self,
            "UserProfiles",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.RETAIN,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Lambda role with necessary permissions
        lambda_role = iam.Role(
            self,
            "PathWeaverLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        # Add necessary permissions to Lambda role
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        self.document_bucket.grant_read_write(lambda_role)
        self.user_table.grant_read_write_data(lambda_role)
        self.vector_store.grant_read_write(lambda_role)

        # Lambda function for path generation
        self.path_generator = lambda_.Function(
            self,
            "PathGenerator",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset("../backend/lambda/path_generator"),
            timeout=Duration.seconds(30),
            memory_size=1024,
            role=lambda_role,
            environment={
                "OPENSEARCH_DOMAIN": self.vector_store.domain_endpoint,
                "USER_TABLE": self.user_table.table_name,
                "DOCUMENT_BUCKET": self.document_bucket.bucket_name,
            },
        )

        # API Gateway
        api = apigw.RestApi(
            self,
            "PathWeaverApi",
            rest_api_name="PathWeaver API",
            description="API for PathWeaver AI learning path generation",
        )

        # API Gateway integration with Lambda
        path_integration = apigw.LambdaIntegration(self.path_generator)
        
        # API endpoints
        api.root.add_resource("generate-path").add_method("POST", path_integration)
        api.root.add_resource("user-profile").add_method("POST", path_integration)
        api.root.add_resource("user-profile").add_method("GET", path_integration) 