from app.infrastructure.embedding import get_embedding_model
from app.infrastructure.qdrant import get_qdrant_client, close_qdrant_client


async def load_infrastructure():
    """
    Load the infrastructure components.
    """
    await get_qdrant_client()
    await get_embedding_model()
    print("Infrastructure loaded successfully.")
    
    
async def unload_infrastructure():
    """
    Unload the infrastructure components.
    """
    await close_qdrant_client()
    print("Infrastructure unloaded successfully.")