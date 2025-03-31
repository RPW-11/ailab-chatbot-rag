from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from fastapi import Depends
from typing import List, Dict, Optional, Any

from .base_repository import VectorDBRepository
from app.config import settings
from app.infrastructure.qdrant import get_qdrant_client

class QdrantRepository(VectorDBRepository):
    def __init__(self, client: AsyncQdrantClient = Depends(get_qdrant_client)):
        self.client = client
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    async def upsert_points(self, points: List[Dict[str, Any]]) -> None:
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point.get("payload", {}),
                )
                for point in points
            ],
        )

    async def delete_point_by_document_id(self, document_id: str) -> None:
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id),
                    )
                ]
            ),
        )
    
    async def search(
        self,
        query_vector: List[float],
        filter: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        search_filter = None

        if filter:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                    for key, value in filter.items()
                ]
            )
        
        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            filter=search_filter,
            limit=limit,
        )
        
        return [
            {
                "id": point.id,
                "score": point.score,
                "payload": point.payload,
            }
            for point in results
        ]
        