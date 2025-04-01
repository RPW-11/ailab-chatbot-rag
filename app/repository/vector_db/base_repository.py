from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from app.schema.indexing_schema import PointSchema


class VectorDBRepository(ABC):
    @abstractmethod
    async def upsert_points(self, points: List[PointSchema]) -> None:
        """
        Upsert points into the collection.
        """
        pass

    @abstractmethod
    async def delete_point_by_document_id(self, document_id: str) -> None:
        """
        Delete points by the document id from the collection.
        """
        pass

    @abstractmethod
    async def search(
        self,
        query_vector: List[float],
        filter: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[PointSchema]:
        """
        Search for points in the collection.
        """
        pass