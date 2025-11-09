# app/api/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Any
from app.services.chat_store import save_text_message, get_chat_history

router = APIRouter()

# 프론트가 보낼 수도 있는 필드를 전부 허용
class ChatMessageIn(BaseModel):
    uid: str
    chat_id: str
    text: Optional[str] = None
    user_message: Optional[str] = None   # 네 프론트가 한 번 이렇게 보냈었음

@router.post("/message")
async def create_message(msg: ChatMessageIn):
    # text, user_message 중 있는 걸로 통일
    final_text = msg.text or msg.user_message
    if not final_text:
        # 아예 내용이 없으면 400 비슷하게 돌려주기
        return {"ok": False, "reason": "text or user_message is required"}

    # 파이어스토어에 저장
    save_text_message(
        uid=msg.uid,
        chat_id=msg.chat_id,
        text=final_text,
    )
    return {"ok": True}

@router.get("/history")
async def history(uid: str, chat_id: str):
    return get_chat_history(uid, chat_id)
