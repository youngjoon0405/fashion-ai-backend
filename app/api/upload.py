from fastapi import APIRouter, UploadFile, File, Form
from app.services.s3 import upload_to_s3
from app.services.chat_store import save_chat_message
from app.services.analysis_results import save_analysis_result
import httpx
import os

router = APIRouter()
AI_URL = os.getenv("AI_SERVER_URL","http://127.0.0.1:9000/analyze")


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
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
    )

    return {
        "image_url": image_url,
        "ai_result": ai_result
    }
