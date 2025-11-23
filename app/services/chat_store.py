# app/services/chat_store.py

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

    나중에 진짜 메시지 저장이 필요해지면
    여기 안에 Firestore / Firebase / RDS 등 원하는 로직을 채우면 됨.
    """
    # 최소한 서버 안 죽게만 해둔 상태
    # print("[CHAT]", user_id, sender, message_type, text, image_url, ai_result)
    return
