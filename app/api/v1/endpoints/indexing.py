from fastapi import APIRouter, Depends, UploadFile
from typing import List
from app.service.indexing_service import IndexingService
from app.schema.indexing_schema import IndexDocumentRequestSchema

router = APIRouter(
    prefix="/indexing",
    tags=["indexing"],
)

@router.post("/documents", status_code=201)
async def index_documents(
    document_files: List[UploadFile], 
    document_body: IndexDocumentRequestSchema = Depends(IndexDocumentRequestSchema.as_form), 
    indexing_service: IndexingService = Depends()
):
    await indexing_service.insert_documents(document_body, document_files)
    return {"message": "Documents indexed successfully."}