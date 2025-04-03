from fastapi import Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schema.inference_schema import InferenceRequestSchema
from app.repository.vector_db.base_repository import VectorDBRepository
from app.repository.vector_db.qdrant_repository import QdrantRepository
from app.infrastructure.llm.llm_interface import LLM
from app.infrastructure.llm.ollama import Ollama


class InferenceService:
    def __init__(
        self,
        vdb_repository: VectorDBRepository = Depends(QdrantRepository),
        llm: LLM = Depends(Ollama)
    ):
        self._vdb_repository = vdb_repository
        self._llm = llm
        
    async def infer(self, inference_body: InferenceRequestSchema):
        # validate input
        input = inference_body.prompt
        
        try:
            await self._llm.change_model(inference_body.model_name)
        
            if inference_body.is_streaming:
                return StreamingResponse(self._llm.astream(input), media_type='text/plain')
            else:
                return await self._llm.ainvoke(input)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))