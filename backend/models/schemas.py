"""
Pydantic schemas for request/response validation.
Defines ChatQueryRequest, ChatResponse, FeedbackRequest, and related models.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime


class ChatQueryRequest(BaseModel):
    """Request schema for chat queries."""
    query_text: str = Field(..., min_length=1, max_length=1000, description="The user's question")
    mode: Literal["full_book", "selection"] = Field(..., description="Query mode (full_book or selection)")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Selected text (required if mode=selection)")
    session_id: Optional[UUID] = Field(None, description="Existing session ID (if continuing conversation)")

    @field_validator('selected_text')
    @classmethod
    def validate_selected_text(cls, v, info):
        """Validate selected_text based on mode."""
        mode = info.data.get('mode')
        if mode == 'selection' and not v:
            raise ValueError("selected_text required for selection mode")
        if mode == 'full_book' and v:
            raise ValueError("selected_text must be null for full_book mode")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query_text": "How do I create a custom ROS 2 message?",
                    "mode": "full_book",
                    "selected_text": None,
                    "session_id": None
                }
            ]
        }
    }


class SourceChunk(BaseModel):
    """Schema for source chunk information in response."""
    chunk_id: UUID = Field(..., description="Unique chunk identifier")
    module_number: int | None = Field(default=None, description="Module number")
    chapter_number: int | None = Field(default=None, description="Chapter number")
    section_title: str = Field(..., description="Section title")
    url: str = Field(..., description="URL to the book page")
    score: float = Field(..., ge=0.0, le=1.0, description="Semantic similarity score (0.0-1.0)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "chunk_id": "550e8400-e29b-41d4-a716-446655440000",
                    "module_number": 1,
                    "chapter_number": 3,
                    "section_title": "Custom Messages and Data Structures",
                    "url": "https://muzaffar401.github.io/Physical-AI-Humanoid-Robotics-Book/docs/module-1/chapter-1-3-custom-messages",
                    "score": 0.89
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response schema for chat queries."""
    response_id: UUID = Field(..., description="Unique response identifier")
    response_text: str = Field(..., description="The chatbot's answer in markdown format")
    source_chunks: list[SourceChunk] = Field(default_factory=list, description="List of book chunks used to generate the response")
    response_time_ms: int = Field(..., gt=0, description="Time taken to generate response (milliseconds)")
    session_id: UUID = Field(..., description="Session ID (for continuing conversation)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response_id": "770e8400-e29b-41d4-a716-446655440002",
                    "response_text": "To create a custom ROS 2 message, you need to...",
                    "source_chunks": [
                        {
                            "chunk_id": "550e8400-e29b-41d4-a716-446655440000",
                            "module_number": 1,
                            "chapter_number": 3,
                            "section_title": "Custom Messages",
                            "url": "https://example.com/module-1/chapter-3",
                            "score": 0.89
                        }
                    ],
                    "response_time_ms": 1850,
                    "session_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            ]
        }
    }


class FeedbackRequest(BaseModel):
    """Request schema for user feedback."""
    response_id: UUID = Field(..., description="ID of the response being rated")
    rating: Literal["positive", "negative"] = Field(..., description="Thumbs up (positive) or thumbs down (negative)")
    feedback_text: Optional[str] = Field(None, max_length=1000, description="Optional text feedback")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response_id": "770e8400-e29b-41d4-a716-446655440002",
                    "rating": "positive",
                    "feedback_text": "This answer was very helpful!"
                }
            ]
        }
    }


class FeedbackResponse(BaseModel):
    """Response schema for feedback submission."""
    feedback_id: UUID = Field(..., description="Unique feedback identifier")
    message: str = Field(default="Feedback recorded successfully", description="Success message")


class SessionCreateRequest(BaseModel):
    """Request schema for creating a new chat session."""
    user_identifier: Optional[str] = Field(None, description="Optional user identifier")


class SessionCreateResponse(BaseModel):
    """Response schema for session creation."""
    session_id: UUID = Field(..., description="Unique session identifier")
    created_at: datetime = Field(..., description="Session creation timestamp")


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    status: str = Field(default="healthy", description="API health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current server timestamp")


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Validation Error",
                    "detail": "selected_text required for selection mode"
                }
            ]
        }
    }
