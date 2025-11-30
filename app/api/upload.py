<<<<<<< HEAD
from fastapi import APIRouter, UploadFile, File, Form
from app.services.s3 import upload_to_s3
from app.services.chat_store import save_chat_message
from app.services.analysis_results import save_analysis_result
import httpx
import os
=======
import os
import httpx
from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from app.services.s3 import upload_fileobj
from app.services.analysis_results import save_ai_result
from app.services.chat_store import save_text_message   # ← 이 이름이 실제 있는 함수
>>>>>>> parent of 97f7a5f (feat: send uid/chat_id to ai server (without secrets))

router = APIRouter()
AI_URL = os.getenv("AI_SERVER_URL","http://127.0.0.1:9000/analyze")

<<<<<<< HEAD
=======
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://localhost:9000/analyze")
>>>>>>> parent of 97f7a5f (feat: send uid/chat_id to ai server (without secrets))

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
<<<<<<< HEAD
    user_id: str = Form(...)
):
    # 1) S3 업로드
    file_bytes = await file.read()
    image_url = upload_to_s3(file_bytes, file.filename)

    # 2) 채팅에 "유저 이미지 메시지" 저장
    save_chat_message(
        user_id=user_id,
        sender="user",
        message_type="image",
        image_url=image_url
    )

    # 3) AI 분석 요청
    async with httpx.AsyncClient(timeout=30) as client:
        ai_resp = await client.post(AI_URL, json={"image_url": image_url})
        ai_result = ai_resp.json()

    # 4) 채팅에도 AI 메시지 저장
    save_chat_message(
        user_id=user_id,
        sender="ai",
        message_type="ai_result",
        content=ai_result.get("summary") if isinstance(ai_result, dict) else None,
        ai_result=ai_result
    )

    # 5) 분석결과 전용 컬렉션에도 저장
    save_analysis_result(
        user_id=user_id,
        image_url=image_url,
        ai_result=ai_result
=======
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
>>>>>>> parent of 97f7a5f (feat: send uid/chat_id to ai server (without secrets))
    )

    return {
        "image_url": image_url,
        "ai_result": ai_result
    }
