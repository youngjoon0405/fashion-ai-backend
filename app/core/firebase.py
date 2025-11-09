# app/core/firebase.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

# EC2에 올려둔 새 키 경로로 '절대경로' 박기
# 실제 파일 이름이랑 경로 맞춰서 넣어
DEFAULT_CRED_PATH = "/home/ec2-user/fashion-ai-backend/hambugibugi-key.json"

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", DEFAULT_CRED_PATH)

print("🔥 using firebase credential:", cred_path)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
print("🔥 connected firestore project:", db.project)
