# app/services/chat_store.py
from datetime import datetime
from app.core.firebase import db

COLLECTION = "chat_messages"

def save_text_message(uid: str, chat_id: str, text: str, sender: str = None):
    doc = {
        "uid": uid,
        "chat_id": chat_id,
        "sender": sender or uid,
        "text": text,
        "type": "text",
        "image_url": None,
        "ai_result": None,
        "created_at": datetime.utcnow().isoformat(),
    }
    db.collection(COLLECTION).add(doc)

def save_image_message(uid: str, chat_id: str, image_url: str, ai_result: dict = None, sender: str = None):
    doc = {
        "uid": uid,
        "chat_id": chat_id,
        "sender": sender or uid,
        "text": "",
        "type": "image",
        "image_url": image_url,
        "ai_result": ai_result,
        "created_at": datetime.utcnow().isoformat(),
    }
    db.collection(COLLECTION).add(doc)

def get_chat_history(uid: str, chat_id: str):
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
