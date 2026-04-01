from fastapi import HTTPException
from deep_translator import GoogleTranslator

def translate_text(text: str, source_lang: str, target_lang: str) -> dict:
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return {"translated": translated, "source": source_lang, "target": target_lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

def get_supported_languages() -> dict:
    return {
        "languages": [
            {"code": "en",    "name": "English",              "flag": "🇬🇧"},
            {"code": "hi",    "name": "Hindi",                "flag": "🇮🇳"},
            {"code": "pa",    "name": "Punjabi",              "flag": "🇮🇳"},
            {"code": "ur",    "name": "Urdu",                 "flag": "🇵🇰"},
            {"code": "es",    "name": "Spanish",              "flag": "🇪🇸"},
            {"code": "fr",    "name": "French",               "flag": "🇫🇷"},
            {"code": "de",    "name": "German",               "flag": "🇩🇪"},
            {"code": "it",    "name": "Italian",              "flag": "🇮🇹"},
            {"code": "pt",    "name": "Portuguese",           "flag": "🇧🇷"},
            {"code": "ru",    "name": "Russian",              "flag": "🇷🇺"},
            {"code": "zh-CN", "name": "Chinese (Simplified)", "flag": "🇨🇳"},
            {"code": "ja",    "name": "Japanese",             "flag": "🇯🇵"},
            {"code": "ko",    "name": "Korean",               "flag": "🇰🇷"},
            {"code": "ar",    "name": "Arabic",               "flag": "🇸🇦"},
            {"code": "bn",    "name": "Bengali",              "flag": "🇧🇩"},
            {"code": "ta",    "name": "Tamil",                "flag": "🇮🇳"},
            {"code": "te",    "name": "Telugu",               "flag": "🇮🇳"},
            {"code": "tr",    "name": "Turkish",              "flag": "🇹🇷"},
            {"code": "nl",    "name": "Dutch",                "flag": "🇳🇱"},
            {"code": "pl",    "name": "Polish",               "flag": "🇵🇱"},
        ]
    }
