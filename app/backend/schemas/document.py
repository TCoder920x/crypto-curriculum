"""Document schemas"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Schema for a single document"""
    id: int
    title: str
    category: str
    filename: str
    file_size: int
    updated_at: datetime
    created_at: datetime
    module_id: Optional[int] = None
    course_scope: Optional[str] = None
    owner: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for document list response"""
    documents: List[DocumentResponse]


class DocumentUploadResponse(DocumentResponse):
    """Upload response schema (alias for now)"""
    pass
