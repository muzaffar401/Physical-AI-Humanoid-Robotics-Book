"""
Embedding service using Sentence Transformers (BAAI/bge-base-en-v1.5).
Generates 768-dimensional embeddings locally without API calls.
"""

from sentence_transformers import SentenceTransformer
from typing import List
import logging
import torch

from config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using sentence-transformers."""

    def __init__(self):
        """Initialize service (model loaded lazily on first use)."""
        self.model_name = settings.embedding_model_name
        self.device = settings.embedding_device
        self.batch_size = settings.embedding_batch_size
        self.model = None
        self._model_loaded = False

    def _load_model(self):
        """Load the embedding model (called on first use)."""
        if self._model_loaded:
            return

        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        logger.info(f"Model loaded successfully on device: {self.device}")

        # Verify embedding dimensions
        test_embedding = self.model.encode("test", convert_to_numpy=True)
        logger.info(f"Embedding dimensions: {len(test_embedding)}")

        if len(test_embedding) != 768:
            raise ValueError(
                f"Expected 768-dim embeddings from {self.model_name}, "
                f"got {len(test_embedding)} dims"
            )

        self._model_loaded = True

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            768-dimensional embedding vector as list of floats
        """
        self._load_model()  # Load model on first use

        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with batching.

        Args:
            texts: List of texts to embed

        Returns:
            List of 768-dimensional embedding vectors
        """
        self._load_model()  # Load model on first use

        try:
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                show_progress_bar=len(texts) > 100  # Show progress for large batches
            )

            logger.info(f"Generated {len(embeddings)} embeddings in batch")
            return [emb.tolist() for emb in embeddings]

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.

        Returns:
            Dict with model name, device, and embedding dimensions
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "embedding_dimensions": 768,
            "batch_size": self.batch_size,
            "model_loaded": self._model_loaded
        }


# Singleton instance
embedding_service = EmbeddingService()
