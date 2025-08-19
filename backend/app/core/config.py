"""
🔧 Configuration settings for AllerScan Backend API
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # App Info
    app_name: str = "AllerScan API"
    app_version: str = "1.0.0"
    description: str = "API for allergen detection from food ingredients"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    allowed_hosts: list = ["*"]
    
    # CORS Settings
    allow_origins: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Vite dev server (alternative port)
        "http://localhost:5175",  # Vite dev server (alternative port)
        "https://yourdomain.vercel.app",  # Production frontend
        "https://Rynrd113.github.io",  # GitHub Pages
        "https://rynrd113.github.io",  # GitHub Pages (lowercase)
    ]
    allow_methods: list = ["GET", "POST", "PUT", "DELETE"]
    allow_headers: list = ["*"]
    
    # Model Paths
    base_dir: Path = Path(__file__).parent.parent
    model_dir: Path = base_dir / "models" / "saved_models"
    
    # Model Files (SVM + AdaBoost)
    svm_adaboost_model_path: str = str(model_dir / "svm_adaboost_model.pkl")
    label_encoder_path: str = str(model_dir / "label_encoder.pkl")
    feature_names_path: str = str(model_dir / "feature_names.pkl")
    model_metadata_path: str = str(model_dir / "model_metadata.json")
    
    # Prediction Settings
    confidence_threshold: float = 0.3
    max_input_length: int = 1000
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/allergen_api.log"
    
    # Database Configuration
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "allerscan_db")
    
    @property
    def database_url(self) -> str:
        """Generate MySQL database URL"""
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
    
    # Performance Settings
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Ensure model files exist (OPTIONAL - model kini dilatih dari dataset asli sesuai script dosen)
def validate_model_files():
    """
    Validate that all required SVM + AdaBoost model files exist
    Sekarang OPTIONAL karena model dilatih langsung dari dataset Excel sesuai script dosen
    """
    required_files = [
        settings.svm_adaboost_model_path,
        settings.label_encoder_path,
        settings.feature_names_path,
        settings.model_metadata_path,
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        # Log warning tapi tidak error karena model sekarang dilatih dari dataset
        print(f"⚠️  Pre-trained model files tidak ditemukan: {missing_files}")
        print("📚 Model akan dilatih dari dataset Excel sesuai script dosen")
        return True
    
    return True

# Export
__all__ = ["settings", "validate_model_files"]
