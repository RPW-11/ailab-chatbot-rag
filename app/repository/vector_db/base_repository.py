from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class VectorDBRepository(ABC):
    @abstractmethod
    async def upsert_points(self, points: List[Dict[str, Any]]) -> None:
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
    ) -> List[Dict[str, Any]]:
        """
        Search for points in the collection.
        """
        pass