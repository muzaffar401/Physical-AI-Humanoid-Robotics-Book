"""
RAG (Retrieval-Augmented Generation) service.
Orchestrates vector search, prompt construction, and response generation.
"""

from typing import List, Dict, Any, Optional
import logging
import time

from services.qdrant_service import qdrant_service
from services.openai_service import openai_service
from services.embedding_service import embedding_service  # Import singleton, not class

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG operations: search, prompt construction, and generation."""

    def __init__(self):
        """Initialize RAG service with dependencies."""
        self.qdrant = qdrant_service
        self.openai = openai_service
        self.embedding = embedding_service  # Use singleton with lazy loading

    async def embed_query(self, query_text: str) -> List[float]:
        """
        Generate embedding for user query using local sentence transformers.

        Args:
            query_text: User's question

        Returns:
            Query embedding vector (768 dimensions)
        """
        return self.embedding.embed_text(query_text)

    async def semantic_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        module_filter: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search in Qdrant.

        Args:
            query_embedding: Query vector
            limit: Number of results
            score_threshold: Minimum similarity
            module_filter: Optional module number filter

        Returns:
            List of relevant chunks with metadata
        """
        return await self.qdrant.search(
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
            module_filter=module_filter
        )

    def construct_prompt(
        self,
        query_text: str,
        context_chunks: List[Dict[str, Any]],
        mode: str = "full_book"
    ) -> List[Dict[str, str]]:
        """
        Construct prompt with system message, context, and user query.

        Args:
            query_text: User's question
            context_chunks: Retrieved chunks from vector search
            mode: Query mode (full_book or selection)

        Returns:
            Messages list for OpenAI API
        """
        # System message
        system_message = """You are a helpful AI assistant for the Physical AI & Humanoid Robotics Book.

Your role:
- Answer questions about ROS 2, robotics, physical AI, and humanoid robotics
- Provide accurate, concise answers based on the book content
- Include specific examples and code snippets when relevant
- If the question is outside the book's scope, politely explain what the book covers

Guidelines:
- Use markdown formatting for code blocks and emphasis
- Cite specific chapters/modules when referencing content
- Be encouraging and supportive to learners
- If unsure, acknowledge limitations rather than guessing"""

        # Context from retrieved chunks
        if mode == "full_book" and context_chunks:
            context_text = "\n\n---\n\n".join([
                f"**Module {chunk['module_number']}, Chapter {chunk['chapter_number']}: {chunk['section_title']}**\n\n{chunk['content_text']}"
                for chunk in context_chunks[:5]  # Use top 5 chunks
            ])

            user_message = f"""Based on the following content from the Physical AI & Humanoid Robotics Book:

{context_text}

---

Question: {query_text}

Please provide a clear, helpful answer based on the content above. Include citations to specific chapters when relevant."""

        else:
            # Selection mode or no context found
            user_message = query_text

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        return messages

    async def generate_answer(
        self,
        query_text: str,
        mode: str = "full_book",
        selected_text: Optional[str] = None,
        module_filter: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate answer using RAG pipeline.

        Args:
            query_text: User's question
            mode: Query mode (full_book or selection)
            selected_text: Selected text (for selection mode)
            module_filter: Optional module filter

        Returns:
            Dict with response_text, source_chunks, response_time_ms
        """
        start_time = time.time()

        try:
            if mode == "selection":
                # Selection mode: use selected text as context
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Answer the user's question based on the provided text selection."
                    },
                    {
                        "role": "user",
                        "content": f"Based on this text:\n\n{selected_text}\n\nQuestion: {query_text}"
                    }
                ]
                source_chunks = []  # No vector search in selection mode

            else:
                # Full book mode: RAG pipeline
                # 1. Generate query embedding
                query_embedding = await self.embed_query(query_text)
                logger.info("Generated query embedding")

                # 2. Search for relevant chunks
                source_chunks = await self.semantic_search(
                    query_embedding=query_embedding,
                    limit=10,
                    score_threshold=0.7,
                    module_filter=module_filter
                )
                logger.info(f"Found {len(source_chunks)} relevant chunks")

                # Check if we found relevant content
                if not source_chunks:
                    return {
                        "response_text": "I couldn't find relevant information in the book to answer your question. This book covers ROS 2, robotics fundamentals, URDF modeling, and physical AI for humanoid robotics. Could you rephrase your question or ask about one of these topics?",
                        "source_chunks": [],
                        "response_time_ms": int((time.time() - start_time) * 1000),
                        "token_usage": {}
                    }

                # 3. Construct prompt with context
                messages = self.construct_prompt(query_text, source_chunks, mode)

            # 4. Generate response
            result = await self.openai.generate_response(messages)
            response_text = result["response_text"]
            token_usage = result["token_usage"]

            # 5. Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            logger.info(f"Generated answer in {response_time_ms}ms")

            return {
                "response_text": response_text,
                "source_chunks": source_chunks[:5],  # Return top 5 for citations
                "response_time_ms": response_time_ms,
                "token_usage": token_usage
            }

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise


# Singleton instance
rag_service = RAGService()
