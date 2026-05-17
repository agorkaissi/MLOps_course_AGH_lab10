# __main__.py

import inspect
import pulumi
import pulumi_aws as aws
import json

# Lambda handler - defined here, deployed below
def handler(event, context):
    import json
    import logging
    import os

    logging.basicConfig(level=logging.INFO)

    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.info(f"Lambda running with LOG_LEVEL={log_level}")

    body = event.get("body")

    if body:
        try:
            body = json.loads(body)
        except Exception:
            body = {}

    name = body.get("name") if isinstance(body, dict) else None

    if not name:
        name = "World"

    message = f"Hello, {name}!"

    logging.info(f"Generated message: {message}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": message})
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
    role=role.arn,
    environment={
        "variables": {
            "LOG_LEVEL": "INFO"
        }
    }
)

pulumi.export("function_name", fn.name)
pulumi.export("function_arn", fn.arn)
