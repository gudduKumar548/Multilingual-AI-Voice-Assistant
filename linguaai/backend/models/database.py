from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config.settings import settings
import datetime


db_url = settings.DATABASE_URL
if db_url and 'sslmode' not in db_url:
    db_url = db_url + '?sslmode=require'

engine = create_engine(
    db_url,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, nullable=False)
    email         = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user_rel", cascade="all, delete")

class Conversation(Base):
    __tablename__ = "conversations"
    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String, ForeignKey("users.username"), nullable=False)
    title      = Column(String, default="New Conversation")
    language   = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_rel   = relationship("User", back_populates="conversations")
    messages   = relationship("Message", back_populates="conversation", cascade="all, delete")

class Message(Base):
    __tablename__ = "messages"
    id              = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    username        = Column(String, nullable=False)
    user_msg        = Column(Text, nullable=False)
    ai_reply        = Column(Text, nullable=False)
    language        = Column(String, default="en")
    created_at      = Column(DateTime, default=datetime.datetime.utcnow)
    conversation    = relationship("Conversation", back_populates="messages")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()