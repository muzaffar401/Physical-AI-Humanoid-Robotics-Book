"""
Configuration management for RAG Chatbot API.
Loads environment variables using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Agents Configuration (for LLM responses)
    openai_api_key: str
    openai_chat_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.3
    openai_max_tokens: int = 1000

    # Sentence Transformers Configuration (for local embeddings)
    embedding_model_name: str = "BAAI/bge-base-en-v1.5"
    embedding_device: str = "cpu"  # or "cuda" if GPU available
    embedding_batch_size: int = 32

    # Qdrant Configuration (768 dimensions for BAAI/bge-base-en-v1.5)
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "book_content"
    qdrant_vector_size: int = 768  # Changed from 1536 to 768

    # Database Configuration
    database_url: str

    # API Server Configuration
    api_host: str = "localhost"
    api_port: int = 8000
    api_version: str = "1.0.0"
    environment: str = "development"

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # Sentry (optional)
    sentry_dsn: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Singleton instance
settings = Settings()
