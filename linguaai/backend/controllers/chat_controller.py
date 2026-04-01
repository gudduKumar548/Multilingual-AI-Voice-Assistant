import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from config.settings import settings
from models.chat_model import save_message, get_recent_messages_for_context

LANG_NAMES = {
    "en": "English", "hi": "Hindi", "pa": "Punjabi", "ur": "Urdu",
    "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "zh-CN": "Chinese", "ja": "Japanese",
    "ko": "Korean", "ar": "Arabic", "bn": "Bengali", "ta": "Tamil",
    "te": "Telugu", "tr": "Turkish", "nl": "Dutch", "pl": "Polish"
}

async def get_ai_response(message: str, target_language: str, username: str, conv_id: int, db: Session) -> str:
    lang_name = LANG_NAMES.get(target_language, "English")

    system_prompt = (
        f"You are a helpful voice assistant. "
        f"IMPORTANT: You MUST ALWAYS respond ONLY in {lang_name}. "
        f"No matter what language the user writes in, your reply must be in {lang_name} only. "
        f"Never switch to any other language. Never mix languages. "
        f"Always use {lang_name} exclusively in every response."
    )

    history = get_recent_messages_for_context(db, conv_id, limit=6)

    messages = [{"role": "system", "content": system_prompt}]
    for h in history:
        messages.append({"role": "user", "content": h.user_msg})
        messages.append({"role": "assistant", "content": h.ai_reply})
    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                settings.GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": 0.7
                }
            )

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid Groq API key.")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Groq error: {response.text}")

        ai_reply = response.json()["choices"][0]["message"]["content"].strip()
        save_message(db, conv_id, username, message, ai_reply, target_language)
        return ai_reply

    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to Groq.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def generate_title(first_message: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                settings.GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": "Generate a very short title (max 5 words) for this conversation. Reply with ONLY the title, nothing else."},
                        {"role": "user", "content": first_message}
                    ],
                    "max_tokens": 20
                }
            )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
    except:
        pass
    return first_message[:30] + ("..." if len(first_message) > 30 else "")