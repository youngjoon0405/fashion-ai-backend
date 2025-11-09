# app/services/s3.py
import boto3
import os

# .env에 있는 값 읽어오기
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
S3_BUCKET = os.getenv("S3_BUCKET")

# boto3 세션 만들기
session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

s3 = session.client("s3")


def upload_fileobj(fileobj, key: str, content_type: str = "image/jpeg"):
    """
    fileobj: 업로드할 파일 객체 (FastAPI의 UploadFile.file)
    key: S3에 저장할 경로/이름
    """
    s3.upload_fileobj(
        fileobj,
        S3_BUCKET,
        key,
        ExtraArgs={"ContentType": content_type},
    )

    # 업로드 후 접근 가능한 URL 만들어서 리턴
    url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
    return url
