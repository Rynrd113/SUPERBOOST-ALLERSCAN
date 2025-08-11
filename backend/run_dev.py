#!/usr/bin/env python3
"""
🚀 Development server runner for AllerScan API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

if __name__ == "__main__":
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting AllerScan API Development Server...")
    print("📁 Working directory:", os.getcwd())
    print("📊 Models location: app/models/saved_models/")
    print("📝 Logs location: logs/")
    print("🌐 API documentation will be available at: http://localhost:8001/docs")
    print("=" * 60)
    
    # Run the development server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
        access_log=True
    )
