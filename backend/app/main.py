"""
🚀 AllerScan FastAPI Application
Main application entry point for allergen detection API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import os

# Import application components
from .api.v1 import api_router
from .core.config import settings, validate_model_files
from .core.logger import api_logger, log_startup, log_error
from .models.inference.predictor import predictor

# Application startup time
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    try:
        # Initialize database and ML models
        api_logger.info("🚀 AllerScan API starting up...")
        
        # Always load from dataset Excel sesuai script dosen
        from .models.inference.predictor import predictor
        
        api_logger.info("📚 Training model from dataset Excel sesuai script notebook dosen...")
        success = predictor.load_and_train_model()
        
        if success:
            api_logger.info("✅ SVM + AdaBoost model loaded successfully from dataset")
            info = predictor.get_model_info()
            api_logger.info(f"📊 Model Info: {info['model_type']}")
            api_logger.info(f"🎯 Features: {info['n_features']}")
            api_logger.info(f"📋 Samples: {info['n_samples']}")
            api_logger.info(f"🔍 CV Accuracy: {info['cv_accuracy_mean']}")
        else:
            api_logger.error("❌ Failed to load SVM + AdaBoost model from dataset")
            api_logger.error("⚠️ API will start but predictions will be unavailable")
    
    except Exception as e:
        api_logger.error(f"❌ Error during model loading: {e}")
        api_logger.error("⚠️ API will start but predictions will be unavailable")
    
    yield
    
    # Cleanup
    api_logger.info("🛑 AllerScan API shutting down...")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# Include API router
app.include_router(
    api_router,
    prefix=settings.api_v1_prefix
)

# Root endpoint
@app.get(
    "/",
    summary="API Root",
    description="Welcome endpoint with basic API information"
)
async def root():
    """API root endpoint"""
    uptime = time.time() - startup_time
    
    return {
        "message": "🔍 Welcome to AllerScan API",
        "description": "AI-powered allergen detection from food ingredients",
        "version": settings.app_version,
        "status": "operational",
        "uptime_seconds": round(uptime, 2),
        "model_loaded": predictor.is_loaded,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "predict": f"{settings.api_v1_prefix}/predict/",
            "health": f"{settings.api_v1_prefix}/health",
            "supported_allergens": f"{settings.api_v1_prefix}/predict/supported-allergens",
            "model_info": f"{settings.api_v1_prefix}/predict/model-info"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    log_error(exc, f"unhandled exception in {request.url}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": time.time()
        }
    )

# HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler for HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "timestamp": time.time()
        }
    )

# Export
__all__ = ["app"]
