"""
Session router.
Handles chat session creation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.schemas import SessionCreateRequest, SessionCreateResponse
from services.database_service import database_service

router = APIRouter()


@router.post("/session", response_model=SessionCreateResponse, status_code=201)
async def create_session(
    request: SessionCreateRequest = SessionCreateRequest(),
    db: Session = Depends(get_db)
):
    """
    Create a new chat session.

    Args:
        request: Optional user_identifier
        db: Database session

    Returns:
        SessionCreateResponse with session_id and created_at
    """
    try:
        session = database_service.create_session(
            db=db,
            user_identifier=request.user_identifier
        )

        return SessionCreateResponse(
            session_id=session.session_id,
            created_at=session.start_timestamp
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")
