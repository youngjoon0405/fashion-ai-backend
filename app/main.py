# app/main.py
from fastapi import FastAPI
from app.core import config  # .env 로드
from app.api import upload, analysis, chat, recommend
from fastapi.middleware.cors import CORSMiddleware  
from app.api import debug

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])  # ← 이 줄 추가

@app.get("/health")
def health():
    return {"status": "ok"}
