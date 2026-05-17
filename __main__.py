import pulumi
from components import RegionalBucket

regions = ["us-east-1", "us-west-2","us-west-1"]

configs = [
    ("us-east-1", 30),
    ("us-west-2", 90),
    ("us-west-1", 90),
]

buckets = [
    RegionalBucket(
        f"{region}",
        region=region,
        bucket_name_prefix="lab-",
        lifecycle_days=days,
    )
    for region, days in configs
]

bucket_arns_by_region = {
    region: bucket.bucket.arn
    for region, bucket in zip(regions, buckets)
}

pulumi.export("bucket_arns_by_region", bucket_arns_by_region)
pulumi.export("bucket_names", [b.bucket.id for b in buckets])
pulumi.export("bucket_arns", [b.bucket.arn for b in buckets])