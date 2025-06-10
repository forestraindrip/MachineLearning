import pulumi
from pulumi_aws import s3

class S3(pulumi.ComponentResource):
    def __init__(self, name: str):
        super().__init__(f'{name}:S3', name)
        bucket = s3.BucketV2(name, bucket=name, )

        # Block public access to the bucket
        public_access_block = s3.BucketPublicAccessBlock(
            f'{name}-public-access-block',
            bucket=bucket.id,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True
        )

        self.bucket_name = bucket.id
