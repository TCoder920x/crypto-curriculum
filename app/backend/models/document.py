"""Document model for reference and uploaded files"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.sql import func
from app.backend.core.database import Base


class Document(Base):
    """Stores reference documents for AI context and downloads"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)  # Original filename
    storage_path = Column(Text, nullable=False)  # Local path on disk
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False, default="user-upload", index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="SET NULL"), nullable=True, index=True)
    course_scope = Column(String(100), nullable=True)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    openai_file_id = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Document(id={self.id}, title='{self.title}', category='{self.category}', uploader_id={self.uploader_id})>"
