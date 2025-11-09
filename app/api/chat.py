# app/api/chat.py
import os
import httpx
from fastapi import APIRouter
from app.services.chat_messages import save_message, get_messages

router = APIRouter()

AI_SERVER_BASE = os.getenv("AI_SERVER_URL_BASE", "http://localhost:9000")

@router.post("/message")
async def send_message(
    chat_id: str,
    user_message: str,
    uid: str = "test_user",
):
    # 1) 유저 메시지 저장 (경로에 uid 추가)
    save_message(
        uid=uid,
        chat_id=chat_id,
        sender=uid,
        text=user_message,
    )

    # 2) AI 서버 호출 (없으면 패스)
    ai_text = "지금은 대화 엔진이 준비 중입니다."
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{AI_SERVER_BASE}/chat",
                json={
                    "chat_id": chat_id,
                    "uid": uid,
                    "user_message": user_message,
                },
            )
        resp.raise_for_status()
        data = resp.json()
        ai_text = data.get("reply", ai_text)
    except Exception:
        pass

    # 3) AI 답장도 같은 경로에 저장
    save_message(
        uid=uid,
        chat_id=chat_id,
        sender="ai",
        text=ai_text,
    )

    return {
        "chat_id": chat_id,
        "user_message": user_message,
        "ai_message": ai_text,
    }


@router.get("/history")
def get_history(chat_id: str, uid: str = "test_user", limit: int = 50):
    messages = get_messages(uid=uid, chat_id=chat_id, limit=limit)
    return {
        "chat_id": chat_id,
        "messages": messages,
    }
