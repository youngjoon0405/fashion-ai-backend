# ai_server/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class AnalyzeReq(BaseModel):
    image_url: str
    uid: Optional[str] = None
    chat_id: Optional[str] = None

@app.post("/analyze")
def analyze(req: AnalyzeReq):
    # 여기선 그냥 더미로 리턴
    return {
        "inputs": {
            "image_url": req.image_url,
            "uid": req.uid,
            "chat_id": req.chat_id,
        },
        "analysis": {
            "main_color": "white",
            "main_material": "denim",
        },
        "fashion_advice": {
            "one_line_summary": "테스트용 응답입니다.",
        },
    }
