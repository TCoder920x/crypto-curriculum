"""Document upload and listing endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import logging
from pathlib import Path
import uuid

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.document import Document
from app.backend.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_TYPES = {ext.strip().lower() for ext in settings.DOCUMENT_ALLOWED_TYPES.split(",")}


def build_document_response(document: Document, owner: str | None = None) -> DocumentResponse:
    """Normalize DB model to API response"""
    updated_at = document.updated_at or document.created_at
    extension = Path(document.filename).suffix.lstrip(".") if document.filename else None
    owner_value = owner
    if not owner_value:
        if document.category == "standard":
            owner_value = "system"
        elif document.uploader_id:
            owner_value = None  # Only fill when we know the username/email
    return DocumentResponse(
        id=document.id,
        title=document.title or Path(document.filename).stem,
        category=document.category or "user-upload",
        filename=document.filename,
        file_size=document.file_size,
        updated_at=updated_at,
        created_at=document.created_at,
        module_id=document.module_id,
        course_scope=document.course_scope,
        owner=owner_value,
        type=extension,
        tags=None,
    )


@router.get("/documents/list", response_model=DocumentListResponse)
async def list_documents(
    module_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return visible documents for the current user"""
    visibility_filter = or_(Document.uploader_id == current_user.id, Document.category == "standard")
    query = (
        select(Document)
        .where(Document.is_deleted == False)  # noqa: E712
        .where(visibility_filter)
        .order_by(Document.updated_at.desc(), Document.created_at.desc())
    )

    if module_id:
        query = query.where(or_(Document.module_id == module_id, Document.module_id.is_(None)))

    result = await db.execute(query)
    documents = result.scalars().all()

    responses = []
    for doc in documents:
        owner = current_user.username or current_user.email if doc.uploader_id == current_user.id else None
        responses.append(build_document_response(doc, owner=owner))

    return DocumentListResponse(documents=responses)


@router.post("/documents/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    module_id: int | None = Form(None),
    course_scope: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a new document and persist metadata"""
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required.")

    extension = Path(file.filename).suffix.lower().lstrip(".")
    if extension not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{extension}'. Allowed types: {', '.join(sorted(ALLOWED_TYPES))}",
        )

    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    storage_dir = Path(settings.DOCUMENT_STORAGE_PATH)
    storage_dir.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid.uuid4().hex}{Path(file.filename).suffix.lower()}"
    storage_path = storage_dir / safe_name
    storage_path.write_bytes(content)

    document = Document(
        title=Path(file.filename).stem,
        filename=file.filename,
        storage_path=str(storage_path.resolve()),
        file_size=len(content),
        mime_type=file.content_type,
        category="user-upload",
        module_id=module_id,
        course_scope=course_scope,
        uploader_id=current_user.id,
    )

    db.add(document)
    await db.commit()
    await db.refresh(document)
    logger.info("Stored document %s uploaded by user %s", document.id, current_user.id)

    owner = current_user.username or current_user.email
    return build_document_response(document, owner=owner)


@router.get("/documents/download/{document_id}")
async def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Download a document if the user has access"""
    result = await db.execute(
        select(Document)
        .where(Document.id == document_id)
        .where(Document.is_deleted == False)  # noqa: E712
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    if document.uploader_id not in (None, current_user.id) and document.category != "standard":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot access this document.")

    file_path = Path(document.storage_path)
    if not file_path.exists():
        logger.error("Document %s missing on disk at %s", document.id, document.storage_path)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document file missing.")

    return FileResponse(
        path=file_path,
        media_type=document.mime_type or "application/octet-stream",
        filename=document.filename or file_path.name,
    )
