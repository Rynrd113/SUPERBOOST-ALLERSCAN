"""
📝 Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class PredictionRequest(BaseModel):
    """Request schema for allergen prediction using SVM + AdaBoost model"""
    
    # Required fields matching the training data format
    nama_produk_makanan: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name",
        example="Kacang Tanah"
    )
    
    bahan_utama: Optional[str] = Field(
        "",
        max_length=200,
        description="Main ingredient",
        example="Kacang Tanah"
    )
    
    pemanis: str = Field(
        ...,
        max_length=100,
        description="Sweetener used",
        example="Gula Aren"
    )
    
    lemak_minyak: str = Field(
        ...,
        max_length=100,
        description="Fat/oil used",
        example="Minyak Sawit"
    )
    
    penyedap_rasa: str = Field(
        ...,
        max_length=100,
        description="Flavor enhancer",
        example="MSG"
    )
    
    alergen: str = Field(
        ...,
        max_length=100,
        description="Known allergen information",
        example="Telur"
    )
    
    # Configuration options
    confidence_threshold: Optional[float] = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for allergen detection"
    )
    
    @validator('nama_produk_makanan')
    def validate_product_name(cls, v):
        """Validate product name"""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()
    
    def to_model_input(self) -> Dict[str, str]:
        """Convert to format expected by SVM + AdaBoost model"""
        return {
            'Nama Produk Makanan': self.nama_produk_makanan,
            'Bahan Utama': self.bahan_utama or self.nama_produk_makanan,  # Use product name if no main ingredient
            'Pemanis': self.pemanis,
            'Lemak/Minyak': self.lemak_minyak,
            'Penyedap Rasa': self.penyedap_rasa,
            'Alergen': self.alergen
        }

class AllergenResult(BaseModel):
    """Individual allergen detection result"""
    
    allergen: str = Field(..., description="Name of the allergen")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    risk_level: str = Field(..., description="Risk level: low, medium, high")
    detected: bool = Field(..., description="Whether allergen was detected")
    
    @validator('risk_level', pre=True, always=True)
    def determine_risk_level(cls, v, values):
        """Determine risk level based on confidence"""
        confidence = values.get('confidence', 0)
        
        if confidence >= 0.7:
            return "high"
        elif confidence >= 0.4:
            return "medium"
        else:
            return "low"

class PredictionResponse(BaseModel):
    """Response schema for allergen prediction"""
    
    success: bool = Field(..., description="Whether prediction was successful")
    
    # Results
    detected_allergens: List[AllergenResult] = Field(
        ..., 
        description="List of detected allergens with confidence scores"
    )
    
    total_allergens_detected: int = Field(
        ..., 
        description="Total number of allergens detected"
    )
    
    # Processing info
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    model_version: str = Field(..., description="Model version used")
    confidence_threshold: float = Field(..., description="Confidence threshold used")
    
    # Input info
    processed_text: str = Field(..., description="Processed input text")
    input_length: int = Field(..., description="Length of input text")
    
    # Risk assessment
    overall_risk: str = Field(..., description="Overall allergen risk: none, low, medium, high")
    overall_confidence: float = Field(0.0, description="Overall confidence score (0.0 to 1.0)")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    
    @validator('overall_risk', pre=True, always=True)
    def determine_overall_risk(cls, v, values):
        """Determine overall risk based on detected allergens"""
        allergens = values.get('detected_allergens', [])
        
        if not allergens:
            return "none"
        
        # Get highest confidence
        max_confidence = max([a.confidence for a in allergens], default=0)
        
        if max_confidence >= 0.7:
            return "high"
        elif max_confidence >= 0.4:
            return "medium"
        else:
            return "low"

class HealthCheckResponse(BaseModel):
    """Health check response schema"""
    
    status: str = Field(..., description="API status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    uptime_seconds: Optional[float] = Field(None, description="API uptime in seconds")

class ErrorResponse(BaseModel):
    """Error response schema"""
    
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

# Export
__all__ = [
    "PredictionRequest", 
    "AllergenResult", 
    "PredictionResponse", 
    "HealthCheckResponse", 
    "ErrorResponse"
]
