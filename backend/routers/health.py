"""
Health check router.
Provides API health status and version information.
"""

from fastapi import APIRouter
from datetime import datetime

from models.schemas import HealthResponse
from config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns API status, version, and timestamp.
    """
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        timestamp=datetime.utcnow()
    )
