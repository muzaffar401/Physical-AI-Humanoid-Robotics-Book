"""
OpenAI API service for embeddings and chat completions.
Handles text embedding generation and LLM response generation.
"""

from openai import AsyncOpenAI
from typing import List, Dict, Any, AsyncIterator
import logging
import asyncio

from config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI async client."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.chat_model = settings.openai_chat_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for text-embedding-3-small)
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for text (length: {len(text)})")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with batching.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call

        Returns:
            List of embedding vectors
        """
        try:
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = await self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)

                logger.info(f"Generated embeddings for batch {i // batch_size + 1} ({len(batch)} texts)")

                # Rate limiting: small delay between batches
                if i + batch_size < len(texts):
                    await asyncio.sleep(0.5)

            return all_embeddings

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> Dict[str, Any]:
        """
        Generate chat completion response.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            Dict with response_text and token_usage
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )

            response_text = response.choices[0].message.content
            token_usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }

            logger.info(f"Generated response ({token_usage['total_tokens']} tokens)")
            return {
                "response_text": response_text,
                "token_usage": token_usage
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def generate_response_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> AsyncIterator[str]:
        """
        Generate chat completion response with streaming.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Yields:
            Text chunks as they arrive
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            logger.info("Completed streaming response")

        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise


# Singleton instance
openai_service = OpenAIService()
