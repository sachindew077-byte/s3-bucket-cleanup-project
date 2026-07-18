import boto3
from datetime import datetime, timedelta, timezone

# Create S3 client
s3 = boto3.client('s3')

# Replace with your bucket name
BUCKET_NAME = "my-first-herobucket"

# TEMPORARY value for testing
# Change this to timedelta(days=30) after testing
AGE_THRESHOLD = timedelta(days=30)


def lambda_handler(event, context):

    now = datetime.now(timezone.utc)

    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=BUCKET_NAME)

    deleted_files = []

    for page in pages:

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            object_key = obj["Key"]
            last_modified = obj["LastModified"]

            age = now - last_modified

            if age > AGE_THRESHOLD:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=object_key
                )

                deleted_files.append(object_key)

                print(f"Deleted: {object_key}")

    return {
        "statusCode": 200,
        "deleted_count": len(deleted_files),
        "deleted_files": deleted_files
    }