from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Settings for the application."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    # App settings
    APP_NAME: str = "ChatbotApp"
    APP_VERSION: str = "1.0.0"

    # API settings
    API_V1_PREFIX: str = "/api/v1"

    # Embedding settings
    EMBEDDING_MODEL_NAME: str = "Alibaba-NLP/gte-multilingual-base"
    EMBEDDING_DIMENSION: int = 768

    # Qdrant settings
    QDRANT_HOST: str = "localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "dev-chatbot-collection"


settings = Settings()
