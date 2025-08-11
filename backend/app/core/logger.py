"""
📝 Logging configuration for AllerScan API
"""

import sys
import os
from pathlib import Path
from loguru import logger
from .config import settings

# Create logs directory if not exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Remove default logger
logger.remove()

# Console logging format
console_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# File logging format
file_format = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level: <8} | "
    "{name}:{function}:{line} | "
    "{message}"
)

# Add console handler
logger.add(
    sys.stderr,
    format=console_format,
    level=settings.log_level,
    colorize=True,
    backtrace=True,
    diagnose=True,
)

# Add file handler
logger.add(
    settings.log_file,
    format=file_format,
    level=settings.log_level,
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    backtrace=True,
    diagnose=True,
)

# API specific logger
api_logger = logger.bind(name="allergen_api")

def log_prediction(input_text: str, predictions: list, processing_time: float):
    """Log prediction details for monitoring"""
    api_logger.info(
        f"Prediction completed | "
        f"Input length: {len(input_text)} chars | "
        f"Allergens found: {len(predictions)} | "
        f"Processing time: {processing_time:.3f}s"
    )

def log_error(error: Exception, context: str = ""):
    """Log errors with context"""
    api_logger.error(f"Error in {context}: {str(error)}")

def log_startup():
    """Log application startup"""
    api_logger.info("🚀 AllerScan API starting up...")
    api_logger.info(f"Environment: {settings.environment}")
    api_logger.info(f"Debug mode: {settings.debug}")
    api_logger.info(f"Model directory: {settings.model_dir}")

def log_model_loaded():
    """Log successful model loading"""
    api_logger.info("✅ ML models loaded successfully")

# Export
__all__ = ["logger", "api_logger", "log_prediction", "log_error", "log_startup", "log_model_loaded"]
