from datetime import datetime
from google.cloud.firestore import Client  # ✅ 이렇게 직접 Client를 가져오는 방식

db = Client()

def save_chat_message(
    user_id: str,
    sender: str,
    message_type: str,
    text: str = None,
    image_url: str = None,
    ai_result: dict = None,
):
    doc_ref = (
        db.collection("chat_messages")
          .document(user_id)
          .collection("messages")
          .document()
    )

    doc_ref.set({
        "uid": user_id,
        "sender": sender,
        "type": message_type,
        "text": text,
        "image_url": image_url,
        "ai_result": ai_result,
        "created_at": datetime.utcnow().isoformat(),
        "chat_id": user_id,
    })
