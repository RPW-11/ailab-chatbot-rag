from fastapi import Depends, HTTPException
from fastapi.responses import StreamingResponse
from sentence_transformers import SentenceTransformer
from app.config import settings
from app.schema.inference_schema import InferenceRequestSchema, Message
from app.repository.vector_db.base_repository import VectorDBRepository
from app.repository.vector_db.qdrant_repository import QdrantRepository
from app.infrastructure.llm.llm_interface import LLM
from app.infrastructure.llm.ollama import Ollama
from app.infrastructure.embedding import get_embedding_model
from app.util.inference_util import build_prompt, format_retrieved_documents, format_conversation_history


class InferenceService:
    def __init__(
        self,
        vdb_repository: VectorDBRepository = Depends(QdrantRepository),
        llm: LLM = Depends(Ollama),
        embedding_model: SentenceTransformer = Depends(get_embedding_model)
    ):
        self._vdb_repository = vdb_repository
        self._llm = llm
        self._embedding_model = embedding_model
        
    async def infer(self, inference_body: InferenceRequestSchema):
        # validate input
        
        system_prompt = settings.SYSTEM_PROMPT
        
        try:
            await self._llm.change_model(inference_body.model_name)

            # retrieval
            question_embedding = self._embedding_model.encode([inference_body.prompt])
            document_points = await self._vdb_repository.search(question_embedding, limit=5)
            retrieved_document_str = format_retrieved_documents(document_points)
            
            input = build_prompt(system_prompt, None, retrieved_document_str, inference_body.prompt)
            
            if inference_body.is_streaming:
                return StreamingResponse(self._llm.astream(input), media_type='text/plain')
            else:
                return await self._llm.ainvoke(input)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))