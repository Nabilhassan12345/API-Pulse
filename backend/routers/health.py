from fastapi import APIRouter
from core.metrics import get_system_metrics

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "metrics": get_system_metrics()
    }

@router.get("/live")
async def liveness_probe():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe():
    # In a real app, this would check DB connections, etc.
    return {"status": "ready"}
