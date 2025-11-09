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

def upload_fileobj(fileobj, key: str, content_type: str = "image/jpeg"):
    s3.upload_fileobj(
        fileobj,
        S3_BUCKET,
        key,
        ExtraArgs={
            "ContentType": content_type,
           
        },
    )
    url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
    return url
