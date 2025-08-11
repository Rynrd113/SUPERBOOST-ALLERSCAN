"""
🛣️ API v1 router configuration - Clean Architecture
"""

from fastapi import APIRouter
from .routes import predict, auth, dataset_clean

# Create main API router
api_router = APIRouter()

# Include routes with clean architecture
api_router.include_router(
    auth.router,
    tags=["Authentication"]
)

api_router.include_router(
    predict.router,
    tags=["Allergen Prediction"]
)

# Use new clean dataset routes
api_router.include_router(
    dataset_clean.router,
    tags=["Dataset Management"]
)

# Health check endpoint
@api_router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the API is running and models are loaded",
    tags=["Health"]
)
async def health_check():
    """Simple health check endpoint"""
    from ...models.inference.predictor import predictor
    
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "model_loaded": predictor.is_loaded,
        "message": "AllerScan API is running"
    }

# Export
__all__ = ["api_router"]
