# app/api/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from app.services import s3

router = APIRouter()

@router.get("/ping")
def ping():
    return {"msg": "upload alive"}

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    # 파일 이름이랑 시간으로 S3 키 만들어주기
    key = f"uploads/{datetime.utcnow().timestamp()}_{file.filename}"

    try:
        url = s3.upload_fileobj(file.file, key, file.content_type)
    except Exception as e:
        # S3 키가 없거나 권한 없으면 여기로 옴
        raise HTTPException(status_code=500, detail=str(e))

    return {"url": url}
