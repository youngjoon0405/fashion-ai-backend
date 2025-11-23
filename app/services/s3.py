# app/services/s3.py
from datetime import datetime
import boto3
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
S3_BUCKET = os.getenv("S3_BUCKET")

session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

s3 = session.client("s3")

def upload_to_s3(fileobj, key: str, content_type: str = "image/jpeg"):
    """
    기존 upload_fileobj 기능을 upload_to_s3 이름으로 그대로 사용
    """
    s3.upload_fileobj(
        fileobj,
        S3_BUCKET,
        key,
        ExtraArgs={
            "ContentType": content_type,
            "ACL": "public-read"
        },
    )

    url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
    return url
