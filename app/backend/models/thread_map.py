"""Thread mapping model for OpenAI conversation management"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.backend.core.database import Base


class ThreadMap(Base):
    """Map conversation_id (frontend) to OpenAI thread_id"""
    __tablename__ = "thread_maps"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, unique=True, nullable=False, index=True)
    thread_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(200), nullable=True)  # User-defined or auto-generated title
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<ThreadMap(conversation_id={self.conversation_id}, thread_id='{self.thread_id}', user_id={self.user_id})>"

