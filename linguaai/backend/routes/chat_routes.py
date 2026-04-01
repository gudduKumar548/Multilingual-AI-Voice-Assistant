from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from controllers.auth_controller import get_current_user
from controllers.chat_controller import get_ai_response, generate_title
from models.database import get_db
from models.chat_model import (
    create_conversation, get_conversations, get_conversation,
    delete_conversation, get_messages, update_conversation_title
)

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    target_language: str = "en"
    conversation_id: Optional[int] = None

class NewConversationRequest(BaseModel):
    language: str = "en"


@router.post("/send")
async def chat(req: ChatRequest, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if not req.conversation_id:
        conv = create_conversation(db, username, "New Conversation", req.target_language)
        conv_id = conv.id
        is_new = True
    else:
        conv = get_conversation(db, req.conversation_id, username)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conv_id = req.conversation_id
        is_new = False

    reply = await get_ai_response(req.message, req.target_language, username, conv_id, db)

    if is_new:
        title = await generate_title(req.message)
        update_conversation_title(db, conv_id, title)
    else:
        title = conv.title

    return {
        "reply": reply,
        "language": req.target_language,
        "conversation_id": conv_id,
        "title": title
    }

@router.post("/new")
async def new_conversation(req: NewConversationRequest, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = create_conversation(db, username, "New Conversation", req.language)
    return {"id": conv.id, "title": conv.title, "language": conv.language}

@router.get("/conversations")
def list_conversations(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    convs = get_conversations(db, username)
    return {"conversations": [
        {"id": c.id, "title": c.title, "language": c.language, "updated_at": str(c.updated_at)}
        for c in convs
    ]}

@router.get("/messages/{conv_id}")
def get_conv_messages(conv_id: int, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = get_conversation(db, conv_id, username)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = get_messages(db, conv_id)
    return {
        "conversation": {"id": conv.id, "title": conv.title, "language": conv.language},
        "messages": [
            {"user_msg": m.user_msg, "ai_reply": m.ai_reply, "language": m.language, "created_at": str(m.created_at)}
            for m in msgs
        ]
    }

@router.delete("/messages/{conv_id}")
def delete_conv(conv_id: int, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_conversation(db, conv_id, username)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": True}