# app/main.py
from fastapi import FastAPI
from app.core import config  # .env 로드
from app.api import upload, analysis, chat, recommend
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 개발 중이면 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])

@app.get("/health")
def health():
    return {"status": "ok"}
