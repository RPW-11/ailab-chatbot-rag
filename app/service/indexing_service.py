from fastapi import Depends, UploadFile, HTTPException
from unstructured.partition.auto import partition
from typing import List
from io import BytesIO
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from app.infrastructure.embedding import get_embedding_model
from app.repository.vector_db.base_repository import VectorDBRepository
from app.repository.vector_db.qdrant_repository import QdrantRepository
from app.schema.indexing_schema import IndexDocumentRequestSchema, PointSchema, PointPayloadSchema
from app.util.indexing_util import validate_document_type


class IndexingService:
    def __init__(
        self, 
        vdb_repository: VectorDBRepository = Depends(QdrantRepository),
        embedding_model: SentenceTransformer = Depends(get_embedding_model)
    ):
        self._vdb_repository = vdb_repository
        self._embedding_model = embedding_model

    async def insert_documents(self, document_body: IndexDocumentRequestSchema, document_files: List[UploadFile]) -> None:
        """
        Insert documents into the vector database.
        """
        if len(document_files) == 0:
            raise HTTPException(400, "No document files provided.")
        if len(document_files) > 5:
            raise HTTPException(400, "Too many document files. Maximum allowed is 5.")
        if len(document_body.document_ids) != len(document_files):
            raise HTTPException(400, "Mismatch between document IDs and document files.")
        if not validate_document_type(document_files):
            raise HTTPException(400, "Invalid document types. Only PDF, DOCX, TXT and IMAGES are allowed.")
        
        for document_file, document_id in zip(document_files, document_body.document_ids):
            file_io = BytesIO(await document_file.read())
            await document_file.close()
            print(f"Processing document: {document_id}")
            elements = partition(file=file_io, strategy="auto")
            embeddings = self._embedding_model.encode([element.text for element in elements], show_progress_bar=True)
            points = [
                PointSchema(
                    id=str(uuid4()),
                    vector=embedding,
                    payload=PointPayloadSchema(
                        document_id=document_id,
                        text=element.text,
                        type='text',
                        page_number=element.metadata.page_number,
                        document_url=document_file.filename,
                    ),
                )
                for embedding, element in zip(embeddings, elements)
            ]
            await self._vdb_repository.upsert_points(points)
            print(f"Indexed document: {document_id} with {len(points)} points.")

    async def delete_document(self, document_id: str) -> None:
        """
        Delete documents from the vector database.
        """
        if not document_id:
            raise HTTPException(400, "No document IDs provided.")
        
        await self._vdb_repository.delete_point_by_document_id(document_id)

        print(f"Deleted points for document ID: {document_id}")