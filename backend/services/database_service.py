"""
Database service for CRUD operations.
Handles sessions, queries, responses, and feedback.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Dict, Any
from uuid import UUID
import logging

from models.database import ChatSession, UserQuery, ChatResponse, UserFeedback, get_db

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database CRUD operations."""

    def create_session(
        self,
        db: Session,
        user_identifier: Optional[str] = None
    ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            db: Database session
            user_identifier: Optional user identifier

        Returns:
            Created ChatSession
        """
        try:
            session = ChatSession(user_identifier=user_identifier)
            db.add(session)
            db.commit()
            db.refresh(session)
            logger.info(f"Created session: {session.session_id}")
            return session

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating session: {e}")
            raise

    def get_session(self, db: Session, session_id: UUID) -> Optional[ChatSession]:
        """Get session by ID."""
        return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    def create_query(
        self,
        db: Session,
        session_id: UUID,
        query_text: str,
        mode: str,
        selected_text: Optional[str] = None,
        embedding: Optional[List[float]] = None
    ) -> UserQuery:
        """
        Create a new user query.

        Args:
            db: Database session
            session_id: Session ID
            query_text: User's question
            mode: Query mode (full_book or selection)
            selected_text: Selected text (for selection mode)
            embedding: Query embedding (optional)

        Returns:
            Created UserQuery
        """
        try:
            query = UserQuery(
                session_id=session_id,
                query_text=query_text,
                mode=mode,
                selected_text=selected_text,
                embedding=embedding
            )
            db.add(query)
            db.commit()
            db.refresh(query)

            # Update session message count
            session = self.get_session(db, session_id)
            if session:
                session.message_count += 1
                db.commit()

            logger.info(f"Created query: {query.query_id}")
            return query

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating query: {e}")
            raise

    def create_response(
        self,
        db: Session,
        query_id: UUID,
        response_text: str,
        source_chunks: Optional[List[Dict[str, Any]]] = None,
        response_time_ms: Optional[int] = None,
        model_used: str = "gpt-4o-mini",
        token_usage: Optional[Dict[str, int]] = None
    ) -> ChatResponse:
        """
        Create a new chat response.

        Args:
            db: Database session
            query_id: Query ID
            response_text: Generated response
            source_chunks: Retrieved chunks (JSONB)
            response_time_ms: Response time in milliseconds
            model_used: Model name
            token_usage: Token usage info (JSONB)

        Returns:
            Created ChatResponse
        """
        try:
            response = ChatResponse(
                query_id=query_id,
                response_text=response_text,
                source_chunks=source_chunks,
                response_time_ms=response_time_ms,
                model_used=model_used,
                token_usage=token_usage
            )
            db.add(response)
            db.commit()
            db.refresh(response)
            logger.info(f"Created response: {response.response_id}")
            return response

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating response: {e}")
            raise

    def create_feedback(
        self,
        db: Session,
        response_id: UUID,
        rating: str,
        feedback_text: Optional[str] = None
    ) -> UserFeedback:
        """
        Create user feedback for a response.

        Args:
            db: Database session
            response_id: Response ID
            rating: Rating (positive or negative)
            feedback_text: Optional text feedback

        Returns:
            Created UserFeedback

        Raises:
            IntegrityError: If feedback already exists for this response
        """
        try:
            feedback = UserFeedback(
                response_id=response_id,
                rating=rating,
                feedback_text=feedback_text
            )
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            logger.info(f"Created feedback: {feedback.feedback_id}")
            return feedback

        except IntegrityError:
            db.rollback()
            logger.warning(f"Feedback already exists for response: {response_id}")
            raise ValueError("Feedback already submitted for this response")

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating feedback: {e}")
            raise

    def get_session_history(
        self,
        db: Session,
        session_id: UUID,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.

        Args:
            db: Database session
            session_id: Session ID
            limit: Maximum number of exchanges to return

        Returns:
            List of {query_text, response_text} dicts
        """
        try:
            queries = (
                db.query(UserQuery)
                .filter(UserQuery.session_id == session_id)
                .order_by(UserQuery.query_timestamp.desc())
                .limit(limit)
                .all()
            )

            history = []
            for query in reversed(queries):  # Reverse to get chronological order
                if query.response:
                    history.append({
                        "role": "user",
                        "content": query.query_text
                    })
                    history.append({
                        "role": "assistant",
                        "content": query.response.response_text
                    })

            return history

        except Exception as e:
            logger.error(f"Error getting session history: {e}")
            raise

    def get_response_by_id(self, db: Session, response_id: UUID) -> Optional[ChatResponse]:
        """Get response by ID."""
        return db.query(ChatResponse).filter(ChatResponse.response_id == response_id).first()

    def get_feedback_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get feedback statistics.

        Returns:
            Dict with positive_rate, total_count, positive_count, negative_count
        """
        try:
            total = db.query(UserFeedback).count()
            positive = db.query(UserFeedback).filter(UserFeedback.rating == "positive").count()
            negative = db.query(UserFeedback).filter(UserFeedback.rating == "negative").count()

            positive_rate = (positive / total * 100) if total > 0 else 0

            return {
                "total_count": total,
                "positive_count": positive,
                "negative_count": negative,
                "positive_rate": round(positive_rate, 2)
            }

        except Exception as e:
            logger.error(f"Error getting feedback stats: {e}")
            raise


# Singleton instance
database_service = DatabaseService()
