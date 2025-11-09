# app/services/chat_messages.py
from datetime import datetime
from typing import Optional, Dict, Any
from app.core.firebase import db

def save_message(
    uid: str,
    chat_id: str,
    sender: str,
    text: str = "",
    image_url: Optional[str] = None,
    ai_result: Optional[Dict[str, Any]] = None,
):
    doc = {
        "chat_id": chat_id,
        "sender": sender,
        "text": text,
        "image_url": image_url,
        "ai_result": ai_result,
        "created_at": datetime.utcnow().isoformat(),
        "type": "image" if image_url else "text",
    }
    # 👇 경로만 user 기준으로 바꾼 것
    (
        db.collection("users")
        .document(uid)
        .collection("chats")
        .document(chat_id)
        .collection("messages")
        .add(doc)
    )


def get_messages(uid: str, chat_id: str, limit: int = 50):
    # 일단 order_by 빼고 파이썬에서 정렬
    q = (
        db.collection("users")
        .document(uid)
        .collection("chats")
        .document(chat_id)
        .collection("messages")
        .limit(limit)
    )
    docs = q.stream()

    messages = []
    for d in docs:
        m = d.to_dict()
        m["id"] = d.id
        messages.append(m)

    messages.sort(key=lambda x: x.get("created_at", ""))
    return messages
