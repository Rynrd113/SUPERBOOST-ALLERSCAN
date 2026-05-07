"""
🚀 Main prediction endpoint for allergen detection - FIXED VERSION
"""

import time
import pandas as pd
from io import BytesIO
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse, StreamingResponse

from ....schemas.request_schemas import (
    PredictionRequest, 
    PredictionResponse, 
    ErrorResponse
)
from ....models.inference.predictor import predictor
from ....core.logger import api_logger, log_prediction, log_error
from ....database.allergen_database import database_manager

# Create router
router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post(
    "/",
    response_model=PredictionResponse,
    summary="Predict allergens from food ingredients",
    description="""
    Analyze food ingredients and predict potential allergens with confidence scores.
    
    **Input format:**
    Required fields matching the SVM + AdaBoost training data:
    - nama_produk_makanan: Product name
    - pemanis: Sweetener type
    - lemak_minyak: Fat/oil type  
    - penyedap_rasa: Flavor enhancer
    - alergen: Known allergen information
    - bahan_utama: (Optional) Main ingredient
    
    **Returns:**
    - Detection result (Terdeteksi/Tidak Terdeteksi) with confidence score
    - Model metadata and processing time
    """,
    responses={
        200: {"description": "Successful prediction"},
        400: {"description": "Invalid input", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
    }
)
async def predict_allergens(request: PredictionRequest, client_request: Request):
    """
    Predict allergens from food ingredient data using SVM + AdaBoost
    """
    start_time = time.time()
    
    try:
        # Check if predictor is loaded
        if not predictor.is_loaded:
            api_logger.error("SVM + AdaBoost predictor not loaded")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model not available. Please try again later."
            )
        
        # Convert request to model input format
        model_input = request.to_model_input()
        
        api_logger.info(f"Processing SVM + AdaBoost prediction for: {request.nama_produk_makanan}")
        
        # Make prediction using form data
        detected_allergens, metadata = predictor.predict_allergens(
            ingredients_data=model_input,
            confidence_threshold=request.confidence_threshold
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Create ingredients string for display
        ingredients_text = f"{request.bahan_utama}, {request.pemanis}, {request.lemak_minyak}, {request.penyedap_rasa}".strip(", ")
        
        overall_confidence = 0.5
        calculated_risk_level = 'none'

        has_allergens = len(detected_allergens) > 0

        # Deteksi spesifik = hasil keyword matching (bukan label generik "Mengandung Alergen")
        has_specific_allergens = has_allergens and any(
            a.allergen != "Mengandung Alergen" for a in detected_allergens
        )

        # OOV check — hanya untuk mengoreksi deteksi GENERIK dari ML model
        is_likely_oov = False
        if 'oov_analysis' in metadata:
            oov_rate = metadata['oov_analysis'].get('oov_rate', 0)
            base_confidence = metadata['oov_analysis'].get('base_confidence', 0)
            if oov_rate >= 90 and abs(base_confidence - 0.6056) < 0.001:
                is_likely_oov = True
                api_logger.warning(f"⚠️ OOV terdeteksi ({oov_rate:.0f}%), base_confidence={base_confidence:.4f}")

        if has_specific_allergens or (has_allergens and not is_likely_oov):
            # Specific keyword detections selalu dipercaya
            # Generic ML detection hanya dipercaya jika bukan OOV
            overall_confidence = sum([a.confidence for a in detected_allergens]) / len(detected_allergens)

            max_confidence = max([a.confidence for a in detected_allergens])
            if max_confidence > 0.8 or len(detected_allergens) > 2:
                calculated_risk_level = 'high'
            elif max_confidence > 0.5 or len(detected_allergens) > 1:
                calculated_risk_level = 'medium'
            else:
                calculated_risk_level = 'low'
        else:
            # Tidak ada alergen spesifik terdeteksi
            if is_likely_oov:
                api_logger.info("✅ OOV generic detection diabaikan — tidak ada keyword match")
                detected_allergens = []
                overall_confidence = 0.78
            else:
                overall_confidence = metadata['oov_analysis'].get('adjusted_confidence', 0.82) \
                    if metadata and 'oov_analysis' in metadata else 0.85
            calculated_risk_level = 'none'
        
        # Update allergen display after potential override
        allergen_display = "tidak terdeteksi" if len(detected_allergens) == 0 else ", ".join([a.allergen for a in detected_allergens])
        
        # Create response
        response = PredictionResponse(
            success=True,
            detected_allergens=detected_allergens,
            total_allergens_detected=len(detected_allergens),
            processing_time_ms=processing_time,
            model_version=metadata['model_version'],
            confidence_threshold=request.confidence_threshold,
            processed_text=ingredients_text,
            input_length=len(ingredients_text),
            overall_risk="",  # Will be auto-computed by validator
            overall_confidence=overall_confidence  # 🔧 FIX: Send calculated confidence to frontend
        )
        
        # Save to database using the new clean database manager
        try:
            # Prepare prediction data for new database structure
            prediction_data = {
                'productName': request.nama_produk_makanan,
                'bahan_utama': request.bahan_utama,
                'pemanis': request.pemanis,
                'lemak_minyak': request.lemak_minyak,
                'penyedap_rasa': request.penyedap_rasa,
                'ingredients': ingredients_text,
                'allergens': allergen_display,
                'allergen_count': len(detected_allergens),
                'confidence': overall_confidence,  # Menggunakan perhitungan confidence yang konsisten dengan frontend
                'risk_level': calculated_risk_level,  # Menggunakan perhitungan risk level yang konsisten dengan frontend
                'processing_time_ms': processing_time,
                'model_version': metadata.get('model_version', 'SVM+AdaBoost'),
                'user_ip': client_request.client.host if client_request.client else '',
                'user_agent': client_request.headers.get('user-agent', '')
            }
            
            # Save using clean database manager
            record_id = database_manager.save_prediction_result(prediction_data)
            api_logger.info(f"✅ Prediction saved with clean architecture - Record ID: {record_id}")
            
        except Exception as db_error:
            api_logger.warning(f"Failed to save to database: {db_error}")
        
        # Log successful prediction
        log_prediction(
            input_text=ingredients_text,
            predictions=detected_allergens,
            processing_time=processing_time / 1000
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Log error
        log_error(e, "prediction endpoint")
        
        # Return error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get(
    "/supported-allergens",
    summary="Get list of supported allergen types",
    description="Returns a list of all allergen types that the model can detect",
    response_model=dict
)
async def get_supported_allergens():
    """
    Get list of allergen types supported by the model
    """
    try:
        if not predictor.is_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model not available"
            )
        
        allergens = predictor.get_supported_allergens()
        
        return {
            "success": True,
            "supported_allergens": allergens,
            "total_count": len(allergens),
            "model_info": predictor.get_model_info()
        }
        
    except HTTPException:
        raise
        
    except Exception as e:
        log_error(e, "supported allergens endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get supported allergens: {str(e)}"
        )

@router.get(
    "/model-info",
    summary="Get ML model information",
    description="Returns detailed information about the loaded ML model",
    response_model=dict
)
async def get_model_info():
    """
    Get information about the loaded ML model
    """
    try:
        model_info = predictor.get_model_info()
        
        return {
            "success": True,
            "model_info": model_info
        }
        
    except Exception as e:
        log_error(e, "model info endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )

@router.get(
    "/dataset-results",
    summary="Get dataset with detection results",
    description="Returns dataset items with their allergen detection results and confidence scores",
    response_model=dict
)
async def get_dataset_results(limit: int = 100):
    """
    Get dataset with allergen detection results
    """
    try:
        # Menggunakan database manager yang tepat untuk prediksi pengguna
        results = database_manager.get_prediction_history(limit=limit)
        stats = database_manager.get_statistics()
        
        return {
            "success": True,
            "dataset_results": results,
            "total_items": len(results),
            "statistics": stats,
            "limit": limit
        }
        
    except Exception as e:
        log_error(e, "dataset results endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dataset results: {str(e)}"
        )

# REMOVED duplicate dataset endpoints - these should only be in dataset.py
# Following DRY principle and clean separation of concerns

# REMOVED: load_dataset_with_predictions endpoint
# Excel dataset should only be used for model training, not loaded into frontend
# Dataset page should only display form prediction results

# REMOVED: download_dataset_excel endpoint  
# This functionality is properly handled in dataset.py with admin authentication
# Following DRY principle - no duplication of dataset management endpoints
        
@router.post(
    "/retrain",
    summary="Retrain model with original + new DB data",
    description="Combines the 399 original training records with all saved predictions, then retrains SVM+AdaBoost.",
    response_model=dict
)
async def retrain_model():
    """
    Retrain the SVM+AdaBoost model using original training data
    combined with all prediction records stored in the database.
    """
    try:
        api_logger.info("🔄 Retrain request received")

        # Get all prediction records from DB to use as additional training data
        all_records_result = database_manager.get_prediction_history(limit=10000)
        all_records = all_records_result.get('records', [])

        api_logger.info(f"📊 Found {len(all_records)} DB records for retraining")

        result = predictor.retrain_with_additional_data(all_records)

        return {
            "success": True,
            "message": f"Model berhasil diretrain dengan {result['total_samples']} data",
            "data": result
        }

    except Exception as e:
        log_error(e, "retrain endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrain gagal: {str(e)}"
        )


# Export
__all__ = ["router"]
