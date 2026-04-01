from fastapi import APIRouter, Depends
from pydantic import BaseModel
from controllers.auth_controller import get_current_user
from controllers.translate_controller import translate_text, get_supported_languages

router = APIRouter(prefix="/api/translate", tags=["Translate"])

class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"

@router.post("/")
def translate(req: TranslateRequest, username: str = Depends(get_current_user)):
    return translate_text(req.text, req.source_lang, req.target_lang)

@router.get("/languages")
def languages():
    return get_supported_languages()
