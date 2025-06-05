"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.BucketV2('my-bucket')

# Turn the bucket into a website:
website = s3.BucketWebsiteConfigurationV2('website',
    bucket=bucket.id,
    index_document={ "suffix": 'index.html'}
)

# Permit access control configuration:
ownership_controls = s3.BucketOwnershipControls('ownership-controls',
    bucket=bucket.id,
    rule={
        'object_ownership': 'ObjectWriter'
    }
)

# Enable public access to the bucket
public_access_block = s3.BucketPublicAccessBlock('public-access-block',
    bucket=bucket.id,
    block_public_acls=False,
)

# Create an S3 bucket object
bucket_object = s3.BucketObject('index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('index.html'),
    content_type='text/html',
    acl='public-read',
    opts=pulumi.ResourceOptions(
        depends_on=[public_access_block, ownership_controls])
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('url', pulumi.Output.concat('http://', website.website_endpoint))
