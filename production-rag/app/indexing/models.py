from pydantic import BaseModel, Field

from app.ingestion.models import Document


class DirectoryLoadResult(BaseModel):
    documents: list[Document]
    files_processed: int = Field(ge=0)
    skipped_files: list[str]


class IndexingResult(BaseModel):
    files_processed: int = Field(ge=0)
    chunks_indexed: int = Field(ge=0)
    skipped_files: list[str]
