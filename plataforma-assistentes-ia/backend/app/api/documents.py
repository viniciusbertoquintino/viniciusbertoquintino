import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import Document, DocumentStatus
from app.services.document_service import process_document

router = APIRouter()

ALLOWED_TYPES = {"pdf", "docx", "xlsx", "txt", "md"}


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(400, f"Tipo não suportado: {ext}. Use: {', '.join(ALLOWED_TYPES)}")

    file_bytes = await file.read()
    doc_id = str(uuid.uuid4())

    doc = Document(
        id=doc_id,
        name=file.filename,
        type=ext,
        status=DocumentStatus.QUEUED,
        size_bytes=len(file_bytes),
    )
    db.add(doc)
    await db.commit()

    background_tasks.add_task(process_document, doc_id, file_bytes, ext, db)

    return {"id": doc_id, "name": file.filename, "status": "na_fila"}


@router.get("/")
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()).limit(50))
    docs = result.scalars().all()
    return [
        {
            "id": str(d.id),
            "name": d.name,
            "type": d.type,
            "status": d.status.value,
            "chunks": d.chunks_count,
            "tokens": d.tokens_count,
            "size": f"{d.size_bytes / 1024:.0f} KB",
            "uploadedAt": d.created_at.strftime("%d/%m/%Y %H:%M"),
        }
        for d in docs
    ]


@router.get("/{doc_id}")
async def get_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    doc = await db.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, "Documento não encontrado")
    return {
        "id": str(doc.id),
        "name": doc.name,
        "type": doc.type,
        "status": doc.status.value,
        "chunks": doc.chunks_count,
        "tokens": doc.tokens_count,
    }


@router.delete("/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    doc = await db.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, "Documento não encontrado")
    await db.delete(doc)
    await db.commit()
    return {"deleted": doc_id}
