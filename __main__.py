# __main__.py

import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket("lab-bucket",
    tags={"Name": "pulumi-lab"}
)

uploaded_file = aws.s3.BucketObject("hello-file",
    bucket=bucket.id,
    key="hello.txt",
    content="Hello from Pulumi!",
    content_type="text/plain"
)

pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
