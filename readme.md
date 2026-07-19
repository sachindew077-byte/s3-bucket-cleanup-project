# Automated S3 Bucket Cleanup Using AWS Lambda

## Project Overview

This project automates the cleanup of stale objects stored in an Amazon S3 bucket using AWS Lambda and Python.

The Lambda function scans all objects in a specified S3 bucket, identifies files older than 30 days, and permanently deletes them. The solution uses the AWS SDK for Python (Boto3) and follows AWS best practices such as paginated object listing and timezone-aware date comparisons.

---

## Objective

Automatically delete objects older than 30 days from an S3 bucket.

---

## Architecture

```text
+-------------+
|   Amazon S3 |
|   Bucket    |
+------+------+
       |
       |
       v
+------------------+
|   AWS Lambda     |
|  (Python 3.12)   |
+------------------+
       |
       |
       v
+------------------+
| CloudWatch Logs  |
+------------------+
```

---

## AWS Services Used

- Amazon S3
- AWS Lambda
- IAM
- Amazon CloudWatch
- Boto3 (AWS SDK for Python)

---

## Project Workflow

1. Create an S3 bucket.
2. Upload files into the bucket.
3. Create an IAM role with the required permissions.
4. Deploy the Lambda function.
5. The Lambda function:
   - Lists all objects using pagination.
   - Compares object timestamps with the current UTC time.
   - Deletes objects older than 30 days.
   - Logs deleted objects to CloudWatch.
6. Verify that only recent files remain in the bucket.

---

## IAM Policy

Attach the following inline policy to the Lambda execution role.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
        },
        {
            "Sid": "DeleteObjects",
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
        }
    ]
}
```

Replace:

```text
YOUR_BUCKET_NAME
```

with your bucket name.

---

## Lambda Function (Python 3.12)

```python
import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

BUCKET_NAME = "your-bucket-name"
DAYS_TO_KEEP = 30


def lambda_handler(event, context):

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_TO_KEEP)

    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=BUCKET_NAME)

    deleted_files = []

    for page in pages:

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            if obj["LastModified"] < cutoff_date:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj["Key"]
                )

                deleted_files.append(obj["Key"])

                print(f"Deleted: {obj['Key']}")

    return {
        "statusCode": 200,
        "deleted_files": deleted_files
    }
```

---

## Testing

Since creating 30-day-old objects is inconvenient during development, the threshold was temporarily reduced to a few minutes for testing.

### Test Steps

1. Upload sample files to the S3 bucket.
2. Change:

```python
timedelta(days=30)
```

to:

```python
timedelta(minutes=5)
```

3. Wait for the threshold to pass.
4. Manually invoke the Lambda function.
5. Verify:
   - Old files are deleted.
   - Recent files remain.
   - CloudWatch logs display deleted file names.

6. Restore the production value:

```python
timedelta(days=30)
```

---

## CloudWatch Verification

Navigate to:

```text
AWS Console → CloudWatch → Log Groups → /aws/lambda/<function-name>
```

Check the logs for:

```text
Deleted: test-file-1.txt
Deleted: sample-image.png
Deleted: old-report.pdf
```

---

## Production Considerations

Amazon S3 Lifecycle Rules can automatically delete old objects without any custom code and are generally the preferred solution.

However, AWS Lambda becomes useful when:

- Object deletion depends on naming conventions or metadata.
- Additional actions are required before deletion (notifications, backups, database updates).
- Cleanup logic involves multiple AWS services or custom business rules.

---

## Best Practices Implemented

✅ Used paginator to handle buckets with large numbers of objects.

✅ Used timezone-aware UTC timestamps.

✅ Followed the principle of least privilege for IAM permissions.

✅ Logged deleted files to CloudWatch.

✅ Parameterized retention duration.

---

## Repository Structure

```text
project-folder/
│
├── lambda_function.py
├── policy.json
├── README.md
└── screenshots/
```

---

## Future Improvements

- Trigger cleanup automatically using EventBridge schedules.
- Store bucket name and retention period in environment variables.
- Send cleanup reports using Amazon SNS.
- Process multiple buckets dynamically.

---

