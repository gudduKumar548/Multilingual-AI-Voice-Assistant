from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import init_db
from routes import auth_router, chat_router, translate_router, tts_router

app = FastAPI(
    title="LinguaAI — Multilingual Voice Assistant",
    description="Free multilingual AI voice assistant powered by Groq + Supabase",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in Supabase on startup
init_db()

# Routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(translate_router)
app.include_router(tts_router)

@app.get("/")
def root():
    return {
        "message": "LinguaAI Backend is running!",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}