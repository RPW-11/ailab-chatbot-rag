from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from fastapi import Depends
from typing import List, Dict, Optional, Any

from .base_repository import VectorDBRepository
from app.config import settings
from app.infrastructure.qdrant import get_qdrant_client
from app.schema.indexing_schema import PointSchema, PointPayloadSchema


class QdrantRepository(VectorDBRepository):
    def __init__(self, client: AsyncQdrantClient = Depends(get_qdrant_client)):
        self.client = client
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    async def upsert_points(self, points: List[PointSchema]) -> None:
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point.id,
                    vector=point.vector,
                    payload=point.payload.model_dump(exclude_none=True),
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
    ) -> List[PointSchema]:
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
        
        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector[0],
            query_filter=search_filter,
            with_payload=True,
            limit=limit,
        )
        
        return [
            PointSchema(
                id=point.id,
                vector=[],
                payload=PointPayloadSchema(
                    document_id=point.payload['document_id'],
                    text=point.payload['text'],
                    type=point.payload['type'],
                    page_number=point.payload['page_number'],
                    img_url=point.payload['img_url'] if 'img_url' in point.payload.keys() else '',
                    document_url=point.payload['document_url'] if 'document_url' in point.payload.keys() else ''
                )
            )
            for point in results.points
        ]
        