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
    # 인덱스 필요 없게 where만 쓰고
    q = db.collection(COLLECTION).where("chat_id", "==", chat_id)
    docs = q.stream()

    msgs = []
    for d in docs:
        data = d.to_dict()
        data["id"] = d.id
        msgs.append(data)

    # 파이썬에서 created_at 기준으로 정렬
    msgs.sort(key=lambda x: x.get("created_at", ""))
    return {"chat_id": chat_id, "messages": msgs}
