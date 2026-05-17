# __main__.py

import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket(
    "lab-bucket",
    tags={"Name": "pulumi-lab"}
)

uploaded_file = aws.s3.BucketObject(
    "index-html",
    bucket=bucket.id,
    key="index.html",
    content="<h1>Hello from Pulumi!</h1>",
    content_type="text/html"
)

website = aws.s3.BucketWebsiteConfiguration(
    "website",
    bucket=bucket.id,
    index_document=aws.s3.BucketWebsiteConfigurationIndexDocumentArgs(
        suffix="index.html"
    )
)

pab = aws.s3.BucketPublicAccessBlock(
    "public-access-block",
    bucket=bucket.id,
    block_public_acls=False,
    block_public_policy=False,
    ignore_public_acls=False,
    restrict_public_buckets=False,
)

policy_document = pulumi.Output.format('{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"{0}/*"}}]}}', bucket.arn)

aws.s3.BucketPolicy(
    "bucket-policy",
     bucket=bucket.id,
     policy=policy_document,
     opts=pulumi.ResourceOptions(depends_on=[pab])
 )

pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
pulumi.export("website_url", website.website_endpoint)

