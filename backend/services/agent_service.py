"""
OpenAI Agents service for generating LLM responses.
Uses OpenAI Agents Python SDK with gpt-4o-mini.
"""

from agents import Agent, Runner
from typing import List, Dict, Any
import logging
import os

from config import settings

logger = logging.getLogger(__name__)


class AgentService:
    """Service for generating responses using OpenAI Agents SDK."""

    def __init__(self):
        """Initialize OpenAI Agent."""
        # Set OpenAI API key for the agents SDK
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        
        self.chat_model = settings.openai_chat_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens
        
        logger.info(f"AgentService initialized with model: {self.chat_model}")

    async def generate_response(
        self,
        system_instructions: str,
        user_message: str,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Generate response using OpenAI Agents SDK.

        Args:
            system_instructions: System-level instructions for the agent
            user_message: User's question
            context: Optional context to include (e.g., retrieved chunks)

        Returns:
            Dict with response_text and usage information
        """
        try:
            # Create agent with instructions
            agent = Agent(
                name="RAG Assistant",
                instructions=system_instructions,
                model=self.chat_model
            )
            
            # Construct full message with context if provided
            if context:
                full_message = f"Context:\n{context}\n\nQuestion: {user_message}"
            else:
                full_message = user_message
            
            # Run agent asynchronously
            result = await Runner.run(agent, full_message)
            
            # Extract response and usage information
            response_text = result.final_output
            usage = result.context_wrapper.usage
            
            token_usage = {
                "requests": usage.requests,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.total_tokens
            }
            
            logger.info(f"Generated response ({token_usage['total_tokens']} tokens)")
            
            return {
                "response_text": response_text,
                "token_usage": token_usage
            }

        except Exception as e:
            logger.error(f"Error generating response with OpenAI Agents: {e}")
            raise

    async def generate_response_with_history(
        self,
        system_instructions: str,
        conversation_history: List[Dict[str, str]],
        context: str = None
    ) -> Dict[str, Any]:
        """
        Generate response with conversation history.

        Args:
            system_instructions: System-level instructions for the agent
            conversation_history: List of previous messages with 'role' and 'content'
            context: Optional context to include (e.g., retrieved chunks)

        Returns:
            Dict with response_text and usage information
        """
        try:
            # Create agent
            agent = Agent(
                name="RAG Assistant",
                instructions=system_instructions,
                model=self.chat_model
            )
            
            # Construct message with history and context
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in conversation_history[:-1]  # Exclude current message
            ])
            
            current_message = conversation_history[-1]['content']
            
            if context:
                full_message = f"Previous conversation:\n{history_text}\n\nContext:\n{context}\n\nCurrent question: {current_message}"
            else:
                full_message = f"Previous conversation:\n{history_text}\n\nCurrent question: {current_message}"
            
            # Run agent
            result = await Runner.run(agent, full_message)
            
            response_text = result.final_output
            usage = result.context_wrapper.usage
            
            token_usage = {
                "requests": usage.requests,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.total_tokens
            }
            
            logger.info(f"Generated response with history ({token_usage['total_tokens']} tokens)")
            
            return {
                "response_text": response_text,
                "token_usage": token_usage
            }

        except Exception as e:
            logger.error(f"Error generating response with history: {e}")
            raise

    def get_model_info(self) -> dict:
        """
        Get information about the agent configuration.

        Returns:
            Dict with model name and parameters
        """
        return {
            "chat_model": self.chat_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }


# Singleton instance
agent_service = AgentService()
