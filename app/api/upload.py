import os
import httpx
from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from app.services.s3 import upload_fileobj
from app.services.analysis_results import save_ai_result
from app.services.chat_store import save_text_message   # ← 이 이름이 실제 있는 함수

router = APIRouter()

AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://localhost:9000/analyze")

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    uid: str = "test_user",
    chat_id: str = "room_1",
):
    key = f"uploads/{datetime.utcnow().timestamp()}_{file.filename}"
    s3_url = upload_fileobj(file.file, key)

    # AI 서버 호출
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(AI_SERVER_URL, json={"image_url": s3_url})
        resp.raise_for_status()
        ai_data = resp.json()
    except Exception as e:
        ai_data = {
            "status": "ai_server_unavailable",
            "image_url": s3_url,
            "error": str(e),
        }

    # 1) 분석 결과 테이블에 저장
    save_ai_result(
        uid=uid,
        image_url=s3_url,
        ai_result=ai_data,
        chat_id=chat_id,
    )

    # 2) 채팅 로그에도 “이미지 올림” 기록 남기기
    # chat_store는 text만 받으니까, 이미지 url을 텍스트로 그냥 넣자
    save_text_message(
        uid=uid,
        chat_id=chat_id,
        text=f"[image] {s3_url}",
    )

    return {
        "image_url": s3_url,
        "ai_result": ai_data,
    }
