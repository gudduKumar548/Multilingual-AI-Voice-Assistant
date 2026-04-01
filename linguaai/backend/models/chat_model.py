from sqlalchemy.orm import Session
from models.database import Conversation, Message
import datetime

# Conversations 
def create_conversation(db: Session, username: str, title: str, language: str):
    conv = Conversation(username=username, title=title, language=language)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversations(db: Session, username: str):
    return db.query(Conversation)\
        .filter(Conversation.username == username)\
        .order_by(Conversation.updated_at.desc())\
        .all()

def get_conversation(db: Session, conv_id: int, username: str):
    return db.query(Conversation)\
        .filter(Conversation.id == conv_id, Conversation.username == username)\
        .first()

def update_conversation_title(db: Session, conv_id: int, title: str):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if conv:
        conv.title = title
        conv.updated_at = datetime.datetime.utcnow()
        db.commit()

def delete_conversation(db: Session, conv_id: int, username: str):
    conv = db.query(Conversation)\
        .filter(Conversation.id == conv_id, Conversation.username == username)\
        .first()
    if conv:
        db.delete(conv)
        db.commit()
        return True
    return False

# Messages
def save_message(db: Session, conv_id: int, username: str, user_msg: str, ai_reply: str, language: str):
    msg = Message(
        conversation_id=conv_id,
        username=username,
        user_msg=user_msg,
        ai_reply=ai_reply,
        language=language
    )
    db.add(msg)
    # update conversation timestamp
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if conv:
        conv.updated_at = datetime.datetime.utcnow()
    db.commit()

def get_messages(db: Session, conv_id: int, limit: int = 50):
    return db.query(Message)\
        .filter(Message.conversation_id == conv_id)\
        .order_by(Message.created_at.asc())\
        .limit(limit)\
        .all()

def get_recent_messages_for_context(db: Session, conv_id: int, limit: int = 6):
    msgs = db.query(Message)\
        .filter(Message.conversation_id == conv_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()
    return list(reversed(msgs))