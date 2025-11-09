# app/api/upload.py
import os
import httpx
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form
from app.services.s3 import upload_fileobj
from app.services.analysis_results import save_ai_result
from app.services.chat_store import save_text_message, save_image_message

router = APIRouter()

AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://127.0.0.1:9000/analyze")

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    uid: str = Form("test_user"),
    chat_id: str = Form("room_1"),
):
    # 1) S3에 올릴 key 만들기
    key = f"uploads/{datetime.utcnow().timestamp()}_{file.filename}"

    # 2) S3 업로드
    s3_url = upload_fileobj(file.file, key)

    # 3) AI 서버 호출 (이번엔 uid, chat_id 같이 보냄!)
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
        # 안되더라도 S3까지는 올라갔으니까 그 정보는 저장
        ai_data = {
            "status": "ai_server_unavailable",
            "image_url": s3_url,
            "error": str(e),
        }

    # 4) 분석 결과 테이블에도 저장 (너가 나중에 조회할 때)
    save_ai_result(
        uid=uid,
        image_url=s3_url,
        ai_result=ai_data,
        chat_id=chat_id,
    )

    # 5) 채팅 타임라인에도 "이미지 보냄"으로 저장
    #    여기서 ai_data도 같이 넣어주면 프론트에서 한 번에 보여줄 수 있음
    save_image_message(
        uid=uid,
        chat_id=chat_id,
        image_url=s3_url,
        ai_result=ai_data,
    )

    # 6) 프론트로 응답
    return {
        "image_url": s3_url,
        "ai_result": ai_data,
    }
