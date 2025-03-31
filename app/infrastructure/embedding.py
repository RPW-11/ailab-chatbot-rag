from sentence_transformers import SentenceTransformer
from app.config import settings

_embedding_model = None

async def get_embedding_model() -> SentenceTransformer:
    """Get the shared embedding model instance"""
    global _embedding_model

    if _embedding_model is None:
        print("Loading embedding model...")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, trust_remote_code=True)
    
    return _embedding_model