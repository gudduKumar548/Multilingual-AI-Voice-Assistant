from gtts import gTTS
from fastapi import HTTPException
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

LANG_MAP = {
    "en": "en", "hi": "hi", "pa": "pa", "ur": "ur",
    "es": "es", "fr": "fr", "de": "de", "it": "it",
    "pt": "pt", "ru": "ru", "zh-CN": "zh-CN", "ja": "ja",
    "ko": "ko", "ar": "ar", "bn": "bn", "ta": "ta",
    "te": "te", "tr": "tr", "nl": "nl", "pl": "pl",
}

def _generate_audio(text: str, lang: str) -> bytes:
    gtts_lang = LANG_MAP.get(lang, "en")
    # Limit text to 200 chars for speed
    text = text[:200]
    tts = gTTS(text=text, lang=gtts_lang, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

async def text_to_speech(text: str, lang: str) -> bytes:
    try:
        loop = asyncio.get_event_loop()
        audio = await loop.run_in_executor(executor, _generate_audio, text, lang)
        return audio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")