#!/usr/bin/env python3
"""
🚀 Replit-compatible entry point for AllerScan API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Import the FastAPI app
from app.main import app

if __name__ == "__main__":
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting AllerScan API for Replit...")
    print("📁 Working directory:", os.getcwd())
    print("📊 Models location: app/models/saved_models/")
    print("📝 Logs location: logs/")
    print("🌐 API documentation will be available at your Replit URL/docs")
    print("=" * 60)
    
    # Get port from environment (Replit sets this automatically)
    port = int(os.environ.get("PORT", 8080))
    
    # Run the server for Replit
    uvicorn.run(
        app,  # Direct app instance
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload for production
        log_level="info",
        access_log=True
    )
