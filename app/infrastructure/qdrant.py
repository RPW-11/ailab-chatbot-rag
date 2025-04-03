from qdrant_client import AsyncQdrantClient, models
from app.config import settings

_client = None 

async def get_qdrant_client() -> AsyncQdrantClient:
    """Get the shared Qdrant client instance"""
    global _client
    
    if _client is None:
        print("Initializing Qdrant client...")
        _client = AsyncQdrantClient(
            url=settings.QDRANT_HOST,
            prefer_grpc=True,
            grpc_port=settings.QDRANT_GRPC_PORT,
            api_key=settings.QDRANT_API_KEY,
        )
        try:
            if not await _client.collection_exists(settings.QDRANT_COLLECTION_NAME):
                await _client.create_collection(
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    vectors_config=models.VectorParams(size=settings.EMBEDDING_DIMENSION, distance=models.Distance.COSINE)
                ) 
        except Exception as e:
            await close_qdrant_client()
            raise ConnectionError(f"Qdrant connection failed: {str(e)}")
    
    return _client 


async def close_qdrant_client():
    """Cleanup for application shutdown"""
    global _client
    if _client:
        await _client.close()
        _client = None