from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from controllers.auth_controller import get_current_user
from controllers.tts_controller import text_to_speech
import io

router = APIRouter(prefix="/api/tts", tags=["TTS"])

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/speak")
async def speak(req: TTSRequest, username: str = Depends(get_current_user)):
    audio_bytes = await text_to_speech(req.text, req.lang)
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"}
    )