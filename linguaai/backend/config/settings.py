from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    GROQ_URL: str = "https://api.groq.com/openai/v1/chat/completions"

    JWT_SECRET: str = os.getenv("JWT_SECRET", "lingua_ai_fixed_secret_key_2024_do_not_change")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", 1440))

    PORT: int = int(os.getenv("PORT", 8000))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

settings = Settings()
