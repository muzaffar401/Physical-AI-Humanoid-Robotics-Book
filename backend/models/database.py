"""
SQLAlchemy database models for RAG Chatbot.
Defines ChatSession, UserQuery, ChatResponse, and UserFeedback tables.
"""

from sqlalchemy import create_engine, Column, String, Integer, Text, CheckConstraint, ForeignKey, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import uuid

from config import settings

# SQLAlchemy Base
Base = declarative_base()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatSession(Base):
    """Chat session model - tracks conversation sessions."""
    __tablename__ = "chat_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_identifier = Column(Text, nullable=True)
    start_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_activity_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    message_count = Column(Integer, default=0, nullable=False)

    # Relationships
    queries = relationship("UserQuery", back_populates="session", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("message_count >= 0", name="message_count_positive"),
        Index("idx_sessions_last_activity", "last_activity_timestamp", postgresql_ops={"last_activity_timestamp": "DESC"}),
        Index("idx_sessions_user", "user_identifier", postgresql_where="user_identifier IS NOT NULL"),
    )


class UserQuery(Base):
    """User query model - stores all user questions."""
    __tablename__ = "user_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.session_id", ondelete="CASCADE"), nullable=False)
    query_text = Column(Text, nullable=False)
    query_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    mode = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    embedding = Column(JSONB, nullable=True)  # Store as JSONB array for now (pgvector can be added later)

    # Relationships
    session = relationship("ChatSession", back_populates="queries")
    response = relationship("ChatResponse", back_populates="query", uselist=False, cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("mode IN ('full_book', 'selection')", name="valid_mode"),
        CheckConstraint(
            "(mode = 'full_book' AND selected_text IS NULL) OR (mode = 'selection' AND selected_text IS NOT NULL)",
            name="selected_text_required_for_selection"
        ),
        Index("idx_queries_session", "session_id", "query_timestamp", postgresql_ops={"query_timestamp": "DESC"}),
        Index("idx_queries_timestamp", "query_timestamp", postgresql_ops={"query_timestamp": "DESC"}),
        Index("idx_queries_mode", "mode"),
    )


class ChatResponse(Base):
    """Chat response model - stores generated responses."""
    __tablename__ = "chat_responses"

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.query_id", ondelete="CASCADE"), nullable=False)
    response_text = Column(Text, nullable=False)
    source_chunks = Column(JSONB, nullable=True)  # Array of {chunk_id, score, module, chapter, url}
    generation_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    response_time_ms = Column(Integer, nullable=True)
    model_used = Column(Text, default="gpt-4o-mini")
    token_usage = Column(JSONB, nullable=True)  # {prompt_tokens, completion_tokens, total_tokens}

    # Relationships
    query = relationship("UserQuery", back_populates="response")
    feedback = relationship("UserFeedback", back_populates="response", uselist=False, cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("response_time_ms > 0", name="response_time_positive"),
        Index("idx_responses_query", "query_id"),
        Index("idx_responses_timestamp", "generation_timestamp", postgresql_ops={"generation_timestamp": "DESC"}),
        Index("idx_responses_time", "response_time_ms"),
    )


class UserFeedback(Base):
    """User feedback model - tracks satisfaction ratings."""
    __tablename__ = "user_feedback"

    feedback_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response_id = Column(UUID(as_uuid=True), ForeignKey("chat_responses.response_id", ondelete="CASCADE"), nullable=False, unique=True)
    rating = Column(Text, nullable=False)
    feedback_text = Column(Text, nullable=True)
    feedback_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    response = relationship("ChatResponse", back_populates="feedback")

    # Constraints
    __table_args__ = (
        CheckConstraint("rating IN ('positive', 'negative')", name="valid_rating"),
        Index("idx_feedback_response", "response_id"),
        Index("idx_feedback_rating", "rating"),
        Index("idx_feedback_timestamp", "feedback_timestamp", postgresql_ops={"feedback_timestamp": "DESC"}),
    )


# Create all tables (for development; use Alembic in production)
def init_db():
    """Initialize database tables (development only)."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Development: Create tables directly
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")
