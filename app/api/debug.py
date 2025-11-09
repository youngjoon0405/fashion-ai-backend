# app/api/debug.py
from fastapi import APIRouter
from app.core.firebase import db

router = APIRouter()

@router.get("/debug/firebase")
def debug_firebase():
    # firestore client가 보고 있는 project 이름을 그대로 돌려줌
    return {
        "firestore_project": db.project
    }
