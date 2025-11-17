"""Query log model for AI chat analytics"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.backend.core.database import Base


class QueryLog(Base):
    """Track all AI chat queries and responses for analytics"""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Query details
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    operation_type = Column(String(50), nullable=True)  # 'chat', 'stream', etc.
    conversation_id = Column(Integer, nullable=True, index=True)
    
    # Metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<QueryLog(id={self.id}, user_id={self.user_id}, conversation_id={self.conversation_id})>"

