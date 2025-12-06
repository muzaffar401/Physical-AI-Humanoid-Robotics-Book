"""
Qdrant vector database service for semantic search.
Handles connection, search, upsert operations.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, Query
from typing import List, Dict, Any, Optional
import uuid
import logging

from config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size

    def create_collection_if_not_exists(self) -> bool:
        """
        Create collection if it doesn't exist.

        Returns:
            bool: True if collection was created, False if it already existed
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return False

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    def create_payload_indices(self) -> None:
        """Create payload indices for filtered search."""
        try:
            # Index for module_number
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="module_number",
                field_schema="integer"
            )

            # Index for chapter_number
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter_number",
                field_schema="integer"
            )

            logger.info("Created payload indices")
        except Exception as e:
            logger.warning(f"Error creating payload indices (may already exist): {e}")

    async def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        module_filter: Optional[int] = None,
        chapter_filter: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks.

        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            score_threshold: Minimum similarity score
            module_filter: Optional module number filter
            chapter_filter: Optional chapter number filter

        Returns:
            List of matching chunks with metadata
        """
        try:
            # Build filter if needed
            query_filter = None
            if module_filter is not None or chapter_filter is not None:
                must_conditions = []
                if module_filter is not None:
                    must_conditions.append(
                        FieldCondition(key="module_number", match=MatchValue(value=module_filter))
                    )
                if chapter_filter is not None:
                    must_conditions.append(
                        FieldCondition(key="chapter_number", match=MatchValue(value=chapter_filter))
                    )
                query_filter = Filter(must=must_conditions)

            # Perform search using query_points (Qdrant client 1.16+ API)
            # query_points returns a QueryResponse with .points attribute
            query_response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,  # Can be a list or Query object
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True
            )
            results = query_response.points

            # Format results
            chunks = []
            for result in results:
                chunks.append({
                    "chunk_id": result.payload.get("chunk_id"),
                    "content_text": result.payload.get("content_text"),
                    "module_number": result.payload.get("module_number"),
                    "chapter_number": result.payload.get("chapter_number"),
                    "section_title": result.payload.get("section_title"),
                    "url": result.payload.get("public_url"),
                    "score": result.score
                })

            logger.info(f"Found {len(chunks)} chunks with score >= {score_threshold}")
            return chunks

        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            raise

    async def upsert_batch(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Upsert a batch of chunks with their embeddings.

        Args:
            chunks: List of dicts with keys: chunk_id, embedding, payload

        Returns:
            Number of chunks upserted
        """
        try:
            points = []
            for chunk in chunks:
                point = PointStruct(
                    id=str(chunk["chunk_id"]),
                    vector=chunk["embedding"],
                    payload=chunk["payload"]
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Upserted {len(points)} chunks")
            return len(points)

        except Exception as e:
            logger.error(f"Error upserting chunks: {e}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information (size, vector count, etc.)."""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise

    def delete_collection(self) -> None:
        """Delete the collection (use with caution)."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise


# Singleton instance
qdrant_service = QdrantService()
