"""
Feedback router.
Handles user feedback (thumbs up/down) for responses.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from models.database import get_db
from models.schemas import FeedbackRequest, FeedbackResponse
from services.database_service import database_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/feedback", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit user feedback for a response.

    Args:
        feedback: Feedback request with response_id, rating, optional text
        db: Database session

    Returns:
        FeedbackResponse with feedback_id

    Raises:
        404: Response not found
        409: Feedback already exists for this response
        500: Internal server error
    """
    try:
        # Verify response exists
        response = database_service.get_response_by_id(db, feedback.response_id)
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")

        # Create feedback
        user_feedback = database_service.create_feedback(
            db=db,
            response_id=feedback.response_id,
            rating=feedback.rating,
            feedback_text=feedback.feedback_text
        )

        logger.info(f"Feedback submitted: {user_feedback.feedback_id}")

        return FeedbackResponse(
            feedback_id=user_feedback.feedback_id,
            message="Feedback recorded successfully"
        )

    except ValueError as e:
        # Duplicate feedback
        raise HTTPException(status_code=409, detail=str(e))

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/feedback")
async def get_feedback_stats(db: Session = Depends(get_db)):
    """
    Get feedback statistics.

    Returns:
        Dict with positive_rate, total_count, positive_count, negative_count
    """
    try:
        stats = database_service.get_feedback_stats(db)
        return stats

    except Exception as e:
        logger.error(f"Error getting feedback stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
