# __main__.py

import pulumi
from components import RegionalBucket

regions = ["us-east-1", "us-west-2"]
buckets = [RegionalBucket(f"lab-{r}", region=r) for r in regions]

pulumi.export("bucket_arns", {r: b.bucket.arn for r, b in zip(regions, buckets)})
