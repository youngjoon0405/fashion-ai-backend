# ai_server/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnalyzeReq(BaseModel):
    image_url: str
    uid: str
    chat_id: str

@app.post("/analyze")
def analyze(req: AnalyzeReq):
    # 여기서는 일단 고정 값 반환 (FastAPI 쪽 파이프라인 테스트용)
    return {
        "inputs": {
            "image_url": req.image_url
        },
        "analysis": {
            "context_pred": "consumer",
            "context_probs": {
                "shop": 0.48,
                "consumer": 0.52
            },
            "main_material": "denim",
            "main_color": "white",
            "items": [
                {
                    "category": "top",
                    "bbox": [134.0, 193.5, 452.1, 751.7],
                    "score": 0.84,
                    "h3_category": "heels",
                    "crop_path": "_e2e_runs/dummy.jpg"
                }
            ],
            "h1_aesthetic_score": 0.0261,
            "h2_outfit_embedding_norm": 2.36
        },
        "fashion_advice": {
            "one_line_summary": "화이트 데님은 깔끔하고 세련된 선택이야.",
            "positive_points": [
                "화이트 데님은 시원해 보여.",
                "다양한 상의와 잘 어울려.",
                "캐주얼하면서도 세련된 느낌을 줘."
            ],
            "suggestion": "화이트 데님에는 미니멀한 상의를 매치해줘."
        }
    }
