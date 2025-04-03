import torch
from sentence_transformers import SentenceTransformer
from app.config import settings

_embedding_model = None

async def get_embedding_model() -> SentenceTransformer:
    """Get the shared embedding model instance"""
    global _embedding_model

    if _embedding_model is None:
        print("Loading embedding model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, device=device, trust_remote_code=True)
    
    return _embedding_model