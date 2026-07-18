# Automated S3 Bucket Cleanup Using AWS Lambda

## Project Objective

Automatically delete stale objects from an S3 bucket that are older than 30 days.

## AWS Services Used

- Amazon S3
- AWS Lambda (Python 3.12)
- IAM
- CloudWatch
- EventBridge (optional)

## Bucket Name

my-first-herobucket

## IAM Permissions

- s3:ListBucket
- s3:DeleteObject

## Lambda Workflow

1. Lambda lists all objects in the bucket using a paginator.
2. The function compares the object's LastModified date with the current UTC time.
3. Objects older than 30 days are deleted.
4. Deleted object names are printed to CloudWatch logs.

## Project Structure

```text
s3-bucket-cleanup-project/
├── lambda_function.py
├── policy.json
├── README.md
└── screenshots/
```

## Testing

For testing, the age threshold was temporarily changed to 5 minutes.

```python
AGE_THRESHOLD = timedelta(minutes=5)
```

Final production configuration:

```python
AGE_THRESHOLD = timedelta(days=30)
```

## Why use Lambda instead of S3 Lifecycle Rules?

S3 Lifecycle Rules are the preferred solution for simple expiration policies because they require no code or compute resources.

Lambda is useful when cleanup depends on custom logic, object naming conventions, tags, or when the deletion process must trigger actions in other AWS services.

## Screenshots

Add screenshots of:

- S3 bucket before cleanup
- IAM role and policy
- Lambda code
- Test execution
- CloudWatch logs
- S3 bucket after cleanup