# app/services/analysis_results.py
from datetime import datetime
from app.core.firebase import db

def save_ai_result(uid: str, image_url: str, ai_result: dict, chat_id: str = "room_1"):
    doc = {
        "uid": uid,
        "chat_id": chat_id,
        "image_url": image_url,
        "ai_result": ai_result,   # ← AI가 준 JSON 그대로 저장
        "created_at": datetime.utcnow().isoformat(),
    }
    db.collection("analysis_results").add(doc)
