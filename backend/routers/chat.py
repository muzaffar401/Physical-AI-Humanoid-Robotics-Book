"""
Chat router.
Handles chat queries and responses using RAG.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

from models.database import get_db
from models.schemas import ChatQueryRequest, ChatResponse, ErrorResponse, SourceChunk
from services.rag_service import rag_service
from services.database_service import database_service
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(
    request: Request,
    query: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Process chat query and return response with citations.

    Args:
        request: FastAPI request (for rate limiting)
        query: Chat query request
        db: Database session

    Returns:
        ChatResponse with answer and source chunks

    Raises:
        400: Validation error
        429: Rate limit exceeded
        500: Internal server error
    """
    try:
        # 1. Create or get session
        if query.session_id:
            session = database_service.get_session(db, query.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
        else:
            session = database_service.create_session(db)

        logger.info(f"Processing query for session: {session.session_id}")

        # 2. Generate answer using RAG
        result = await rag_service.generate_answer(
            query_text=query.query_text,
            mode=query.mode,
            selected_text=query.selected_text
        )

        # 3. Save query to database
        user_query = database_service.create_query(
            db=db,
            session_id=session.session_id,
            query_text=query.query_text,
            mode=query.mode,
            selected_text=query.selected_text
        )

        # 4. Save response to database
        # Format source_chunks for database (convert to dicts for JSONB)
        source_chunks_db = [
            {
                "chunk_id": str(chunk["chunk_id"]) if "chunk_id" in chunk else None,
                "module_number": chunk.get("module_number"),
                "chapter_number": chunk.get("chapter_number"),
                "section_title": chunk.get("section_title"),
                "url": chunk.get("url"),
                "score": chunk.get("score")
            }
            for chunk in result["source_chunks"]
        ]

        chat_response = database_service.create_response(
            db=db,
            query_id=user_query.query_id,
            response_text=result["response_text"],
            source_chunks=source_chunks_db,
            response_time_ms=result["response_time_ms"],
            token_usage=result.get("token_usage")
        )

        # 5. Format response
        # Convert source chunks to Pydantic models
        source_chunks_response = [
            SourceChunk(
                chunk_id=chunk["chunk_id"],
                module_number=chunk["module_number"],
                chapter_number=chunk["chapter_number"],
                section_title=chunk["section_title"],
                url=chunk["url"],
                score=chunk["score"]
            )
            for chunk in result["source_chunks"]
        ]

        return ChatResponse(
            response_id=chat_response.response_id,
            response_text=chat_response.response_text,
            source_chunks=source_chunks_response,
            response_time_ms=chat_response.response_time_ms,
            session_id=session.session_id
        )

    except HTTPException:
        raise

    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Internal server errors
        logger.error(f"Error processing chat query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/chat/selection", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat_selection(
    request: Request,
    query_text: str,
    selected_text: str,
    session_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Convenience endpoint for selection mode queries.

    Args:
        request: FastAPI request
        query_text: User's question
        selected_text: Selected text from page
        session_id: Optional session ID
        db: Database session

    Returns:
        ChatResponse
    """
    chat_query = ChatQueryRequest(
        query_text=query_text,
        mode="selection",
        selected_text=selected_text,
        session_id=session_id
    )

    return await chat(request, chat_query, db)
