"""System/introspection endpoints: /api/system/models."""
from fastapi import APIRouter

from app.core.model_manager import model_manager
from app.schemas.sentiment import ModelAvailability, SystemModelsResponse

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/models", response_model=SystemModelsResponse)
def get_models():
    availability = model_manager.availability()
    return SystemModelsResponse(
        models=[ModelAvailability(**info) for info in availability.values()]
    )
