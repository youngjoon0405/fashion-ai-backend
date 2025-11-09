# app/api/upload.py
import os
import httpx
from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from app.services.s3 import upload_fileobj
from app.services.analysis_results import save_ai_result
from app.services.chat_messages import save_message  # 수정된 서비스

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
            resp = await client.post(
                AI_SERVER_URL,
                json={
                    "image_url": s3_url,
                    "uid": uid,
                    "chat_id": chat_id,
                },
            )
        resp.raise_for_status()
        ai_data = resp.json()
    except Exception as e:
        ai_data = {
            "status": "ai_server_unavailable",
            "image_url": s3_url,
            "error": str(e),
        }

    # 분석 결과 테이블에도 저장 (네가 따로 쓰는 용도)
    save_ai_result(
        uid=uid,
        image_url=s3_url,
        ai_result=ai_data,
        chat_id=chat_id,
    )

    # 👇 대화 타임라인에도 저장 (이제는 /users/{uid}/chats/{chat_id}/messages 밑으로)
    save_message(
        uid=uid,
        chat_id=chat_id,
        sender=uid,
        image_url=s3_url,
        ai_result=ai_data,
    )

    return {
        "image_url": s3_url,
        "ai_result": ai_data,
    }
