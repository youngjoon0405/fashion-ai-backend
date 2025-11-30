<<<<<<< HEAD
# app/services/chat_store.py

=======
>>>>>>> parent of 97f7a5f (feat: send uid/chat_id to ai server (without secrets))
from datetime import datetime

def save_chat_message(
    user_id: str,
    sender: str,
    message_type: str,
    text: str = None,
    image_url: str = None,
    ai_result: dict = None,
):
    """
    🔧 임시 버전: Firestore 같은 외부 DB 전혀 안 쓰고,
    그냥 서버가 안 죽도록 비워둔 함수.

<<<<<<< HEAD
    나중에 진짜 메시지 저장이 필요해지면
    여기 안에 Firestore / Firebase / RDS 등 원하는 로직을 채우면 됨.
    """
    # 최소한 서버 안 죽게만 해둔 상태
    # print("[CHAT]", user_id, sender, message_type, text, image_url, ai_result)
    return
=======
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
>>>>>>> parent of 97f7a5f (feat: send uid/chat_id to ai server (without secrets))
