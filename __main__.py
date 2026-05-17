# __main__.py

import inspect
import pulumi
import pulumi_aws as aws
import json

# Lambda handler - defined here, deployed below
def handler(event, context):
    import json
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Pulumi Lambda!"})
    }

# IAM role for Lambda
role = aws.iam.Role("lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    })
)

aws.iam.RolePolicyAttachment("lambda-basic-execution",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

lambda_source = f"""
import json

{inspect.getsource(handler)}
"""

fn = aws.lambda_.Function(
    "lab-function",
    code=pulumi.AssetArchive({
        "index.py": pulumi.StringAsset(lambda_source)
        }),
    runtime=aws.lambda_.Runtime.PYTHON3D11,
    handler="index.handler",
    role=role.arn
)

pulumi.export("function_name", fn.name)
pulumi.export("function_arn", fn.arn)
