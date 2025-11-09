# app/services/chat_store.py
from datetime import datetime
from app.core.firebase import db

COLLECTION = "chat_messages"

def save_text_message(uid: str, chat_id: str, text: str):
    doc = {
        "uid": uid,
        "chat_id": chat_id,
        "sender": uid,
        "text": text,
        "type": "text",
        "image_url": None,
        "created_at": datetime.utcnow().isoformat(),
    }
    db.collection(COLLECTION).add(doc)

def get_chat_history(uid: str, chat_id: str):
    # uid는 일단 안 쓰고 chat_id 기준으로 다 가져오기
    q = (
        db.collection(COLLECTION)
        .where("chat_id", "==", chat_id)
        .order_by("created_at")
    )
    docs = q.stream()
    msgs = []
    for d in docs:
        data = d.to_dict()
        data["id"] = d.id
        msgs.append(data)
    return {"chat_id": chat_id, "messages": msgs}
