"""
Health check endpoints.
"""
from fastapi import APIRouter, status
from datetime import datetime

from backend.core.config import get_settings
from backend.models.schemas import HealthCheckResponse

router = APIRouter()
settings = get_settings()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is healthy and can connect to Gemini"
)
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and Gemini API availability.
    """
    # Basic health check
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "environment": settings.app_env,
        "gemini_model": settings.gemini_model
    }
    
    # Try to check Gemini connection (optional, can be expensive)
    gemini_available = True
    try:
        from backend.reasoning import GeminiClient
        client = GeminiClient()
        # Just check if client initializes, don't actually call API
        gemini_available = client.client is not None
    except Exception:
        gemini_available = False
    
    health_status["gemini_available"] = gemini_available
    
    return HealthCheckResponse(**health_status)


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness check",
    description="Check if the API is ready to accept requests"
)
async def readiness_check():
    """
    Readiness check endpoint for Kubernetes/load balancers.
    """
    return {"ready": True}


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness check",
    description="Check if the API is alive"
)
async def liveness_check():
    """
    Liveness check endpoint for Kubernetes/load balancers.
    """
    return {"alive": True}
