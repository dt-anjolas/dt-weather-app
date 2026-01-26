"""Health check endpoints for Cloud Run."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for load balancer probes."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check endpoint."""
    return {"status": "ready"}
