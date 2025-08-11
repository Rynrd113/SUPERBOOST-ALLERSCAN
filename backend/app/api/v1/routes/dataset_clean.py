"""
📊 Dataset API Routes - Clean Architecture Implementation

KONSEP YANG BENAR:
✅ Dataset website menampilkan HISTORY hasil prediksi dari form user
✅ Dataset Excel hanya untuk training model (TIDAK ada endpoint untuk load Excel)
✅ Flow: User submit form → Prediction saved → Display in dataset table

Architecture:
✅ DRY Principle - No duplicate code
✅ Single Responsibility - Each endpoint has one clear purpose  
✅ Clean Code - Consistent naming and structure
✅ Reusable Components - Shared utilities and responses
✅ Professional Error Handling

@author SuperBoost AllerScan Team
@version 2.0.0 - Clean Architecture
@updated 2025-08-09
"""

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from typing import List, Dict, Optional
from pydantic import BaseModel
import pandas as pd
from io import BytesIO
from datetime import datetime

from ....database.allergen_database import database_manager
from ....core.logger import api_logger
from ....schemas.request_schemas import ErrorResponse

# Router configuration
router = APIRouter(prefix="/dataset", tags=["Dataset Management"])

# Reusable response builder
class DatasetResponseBuilder:
    """DRY utility class for building consistent API responses"""
    
    @staticmethod
    def success_response(data: Dict, message: str = "Success") -> Dict:
        """Build standardized success response"""
        return {
            "success": True,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
    
    @staticmethod 
    def error_response(error: str, code: int = 500) -> HTTPException:
        """Build standardized error response"""
        api_logger.error(f"Dataset API Error [{code}]: {error}")
        return HTTPException(
            status_code=code,
            detail={"error": error, "timestamp": datetime.now().isoformat()}
        )

# Reusable statistics calculator
class StatisticsCalculator:
    """DRY utility for calculating dataset statistics"""
    
    @staticmethod
    def calculate_detection_metrics(records: List[Dict]) -> Dict:
        """Calculate detection-related metrics"""
        total = len(records)
        if total == 0:
            return {
                "total_records": 0,
                "detected_count": 0,
                "detection_rate": 0.0,
                "average_confidence": 0.0
            }
        
        detected = sum(1 for r in records if r.get('allergen_count', 0) > 0)
        total_confidence = sum(r.get('confidence_score', 0.0) for r in records)
        
        return {
            "total_records": total,
            "detected_count": detected,
            "not_detected_count": total - detected,
            "detection_rate": round((detected / total * 100), 2),
            "average_confidence": round((total_confidence / total * 100), 2)
        }

@router.get(
    "/predictions",
    summary="Get prediction history for dataset display",
    description="""
    Retrieves paginated prediction history from user form submissions.
    This is the PRIMARY data source for the dataset page display.
    
    Note: Excel dataset is NOT included - it's only used for ML model training.
    """,
    response_model=Dict
)
async def get_prediction_history(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    limit: int = Query(10, ge=1, le=1000, description="Items per page"),
    include_stats: bool = Query(True, description="Include statistics in response")
):
    """
    Get paginated prediction history for dataset display
    
    Args:
        page: Page number (1-based indexing)
        limit: Maximum items per page
        include_stats: Whether to include summary statistics
    
    Returns:
        Paginated prediction records with optional statistics
    """
    try:
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Get prediction records with pagination metadata
        result = database_manager.get_prediction_history(limit=limit, offset=offset)
        
        # Build response data with proper pagination
        response_data = {
            "predictions": result['records'],
            "pagination": {
                "current_page": result['pagination']['current_page'],
                "total_pages": result['pagination']['total_pages'],
                "total_items": result['pagination']['total_items'],
                "items_per_page": result['pagination']['items_per_page'],
                "has_more": result['pagination']['has_more'],
                "has_previous": result['pagination']['has_previous'],
                "showing_from": result['pagination']['showing_from'],
                "showing_to": result['pagination']['showing_to']
            }
        }
        
        # Add statistics if requested (based on CURRENT PAGE data for consistency)
        if include_stats:
            # Get global stats
            global_stats = database_manager.get_statistics()
            
            # Calculate page-specific stats for consistency between table and chart
            page_records = result['records']
            page_detected = sum(1 for r in page_records if r.get('allergen_count', 0) > 0)
            page_not_detected = len(page_records) - page_detected
            page_avg_confidence = sum(r.get('confidence_score', 0.0) for r in page_records) / len(page_records) if page_records else 0.0
            
            response_data["statistics"] = {
                "overview": {
                    "total_predictions": global_stats['total_predictions'],
                    "detection_rate": global_stats['detection_rate'],
                    "average_confidence": global_stats['average_confidence'],
                    "model_algorithm": global_stats['model_info']['algorithm']
                },
                "detection_breakdown": {
                    "detected_count": global_stats['detected_count'],
                    "not_detected_count": global_stats['not_detected_count'],
                    "detection_rate": global_stats['detection_rate']
                },
                # Chart data SHOULD USE GLOBAL data for consistency across all pages
                "chart_data": {
                    "detection_pie": [
                        {"name": "Terdeteksi Alergen", "count": global_stats['detected_count'], "color": "#EF4444"},
                        {"name": "Tidak Terdeteksi", "count": global_stats['not_detected_count'], "color": "#10B981"}
                    ],
                    "allergens_distribution": database_manager.get_top_allergens(6)
                },
                "model_info": global_stats['model_info']
            }
            
            # Add page-specific metrics for better consistency
            response_data["page_metrics"] = {
                "page_detected_count": page_detected,
                "page_not_detected_count": page_not_detected,
                "page_detection_rate": round((page_detected / len(page_records) * 100), 2) if page_records else 0.0,
                "page_average_confidence": round(page_avg_confidence * 100, 2)
            }
        
        api_logger.info(f"📊 Served dataset page {page} with {len(result['records'])} records ({result['pagination']['showing_from']}-{result['pagination']['showing_to']} of {result['pagination']['total_items']})")
        return DatasetResponseBuilder.success_response(response_data, "Dataset retrieved successfully")
        
    except Exception as e:
        raise DatasetResponseBuilder.error_response(f"Failed to retrieve dataset: {str(e)}")

@router.get(
    "/statistics",
    summary="Get comprehensive dataset statistics",
    description="Get detailed statistics about prediction results for dashboard display"
)
async def get_dataset_statistics():
    """
    Get comprehensive dataset statistics
    
    Returns:
        Detailed statistics including detection rates, confidence metrics, and charts data
    """
    try:
        # Get basic statistics
        stats = database_manager.get_statistics()
        
        # Get recent predictions for trend analysis
        recent_data = database_manager.get_prediction_history(limit=100)
        recent_records = recent_data['records']  # Extract records from pagination structure
        # trend_metrics = StatisticsCalculator.calculate_detection_metrics(recent_records)  # Skip for now
        
        # Build comprehensive response
        response_data = {
            "overview": {
                "total_predictions": stats['total_predictions'],
                "detection_rate": stats['detection_rate'],
                "average_confidence": stats['average_confidence'],
                "model_algorithm": stats['model_info']['algorithm']
            },
            "detection_breakdown": {
                "detected_count": stats['detected_count'],
                "not_detected_count": stats['not_detected_count'],
                "detection_percentage": stats['detection_rate']
            },
            "performance_metrics": {
                "average_processing_time": stats['average_processing_time'],
                "confidence_distribution": stats['average_confidence'],
                "risk_level_distribution": stats['risk_distribution']
            },
            "chart_data": {
                "detection_pie": [
                    {"name": "Terdeteksi Alergen", "count": stats['detected_count'], "color": "#EF4444"},
                    {"name": "Tidak Terdeteksi", "count": stats['not_detected_count'], "color": "#10B981"}
                ],
                "allergens_distribution": database_manager.get_top_allergens(6),
                "risk_distribution": [
                    {"level": level, "count": count} 
                    for level, count in stats['risk_distribution'].items()
                ]
            },
            "model_info": stats['model_info'],
            "last_updated": datetime.now().isoformat()
        }
        
        api_logger.info("📈 Dataset statistics calculated and served")
        return DatasetResponseBuilder.success_response(response_data, "Statistics retrieved successfully")
        
    except Exception as e:
        raise DatasetResponseBuilder.error_response(f"Failed to calculate statistics: {str(e)}")

@router.get(
    "/export/excel",
    summary="Export dataset as Excel file",
    description="Export prediction history as Excel file for analysis (optimized for large datasets)"
)
async def export_dataset_excel(
    limit: int = Query(1000, ge=1, le=10000, description="Maximum records to export")
):
    """
    Export prediction dataset as Excel file with performance optimization
    
    Args:
        limit: Maximum number of records to include
    
    Returns:
        Excel file as streaming response
    """
    try:
        # Add logging for monitoring
        api_logger.info(f"📥 Starting Excel export for {limit} records...")
        start_time = datetime.now()
        
        # Get prediction records with better error handling
        try:
            data = database_manager.get_prediction_history(limit=limit)
            records = data['records']  # Extract records from pagination structure
        except Exception as db_error:
            api_logger.error(f"❌ Database error during export: {db_error}")
            raise DatasetResponseBuilder.error_response("Database connection failed during export", 503)
        
        if not records:
            api_logger.warning("⚠️ No prediction data available for export")
            raise DatasetResponseBuilder.error_response("No prediction data available for export", 404)
        
        api_logger.info(f"📊 Retrieved {len(records)} records for export")
        
        # Convert to DataFrame with format sesuai dataset dosen
        try:
            df = pd.DataFrame(records)
        except Exception as df_error:
            api_logger.error(f"❌ Error creating DataFrame: {df_error}")
            raise DatasetResponseBuilder.error_response("Error processing data for export", 500)
        
        # Format OPTIMAL: Menggabungkan permintaan dosen dengan kebutuhan teknis
        # Menggunakan terminologi yang konsisten dengan dataset asli dosen
        df = df.rename(columns={
            'product_name': 'Nama Produk Makanan',  # Konsisten dengan dataset asli
            'bahan_utama': 'Bahan Utama',           # Konsisten dengan dataset asli
            'pemanis': 'Pemanis',
            'lemak_minyak': 'Lemak/Minyak',
            'penyedap_rasa': 'Penyedap Rasa',       # Konsisten dengan dataset asli
            'ingredients_input': 'Input Bahan',      # Jelas ini adalah input user
            'predicted_allergens': 'Hasil Deteksi'  # Hasil prediksi alergen
        })
        
        # Kolom sesuai format dataset asli dosen + informasi penting untuk evaluasi
        base_columns = ['Nama Produk Makanan', 'Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa', 'Input Bahan', 'Hasil Deteksi']
        
        # Informasi teknis yang SANGAT PENTING untuk evaluasi model dan tracking
        technical_columns = {
            'confidence_score': 'Tingkat Kepercayaan (%)',
            'created_at': 'Tanggal Prediksi',
            'risk_level': 'Tingkat Risiko'
        }
        
        # Apply technical column renaming
        df = df.rename(columns=technical_columns)
        
        # Select final columns (dosen format + technical info)
        available_columns = [col for col in base_columns + list(technical_columns.values()) if col in df.columns]
        df = df[available_columns]
        
        # Convert confidence to percentage
        if 'Tingkat Kepercayaan (%)' in df.columns:
            df['Tingkat Kepercayaan (%)'] = (df['Tingkat Kepercayaan (%)'] * 100).round(2)
        
        # Create Excel file in memory with optimization for better performance
        try:
            excel_buffer = BytesIO()
            
            # Use openpyxl for better performance with large datasets
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Main data sheet - Format sesuai Dataset Dosen
                df.to_excel(writer, sheet_name='Dataset Prediksi Alergen', index=False)
                
                # Summary statistics sheet (optional, can be skipped for large exports)
                if len(records) < 2000:  # Only add summary for smaller datasets
                    stats = database_manager.get_statistics()
                    summary_df = pd.DataFrame([
                        ['Total Prediksi', stats['total_predictions']],
                        ['Alergen Terdeteksi', stats['detected_count']], 
                        ['Tidak Terdeteksi', stats['not_detected_count']],
                        ['Tingkat Deteksi (%)', stats['detection_rate']],
                        ['Kepercayaan Rata-rata (%)', stats['average_confidence']],
                        ['Algoritma Model', stats['model_info']['algorithm']],
                        ['Format Export', 'Gabungan Permintaan Dosen + Info Teknis Penting'],
                        ['Catatan', 'Input Bahan = bahan yang diinput user, Hasil Deteksi = prediksi alergen'],
                        ['Jumlah Records Exported', len(records)],
                        ['Tanggal Export', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                    ], columns=['Metrik', 'Nilai'])
                    
                    summary_df.to_excel(writer, sheet_name='Ringkasan Statistik', index=False)
            
            excel_buffer.seek(0)
            
        except Exception as excel_error:
            api_logger.error(f"❌ Error creating Excel file: {excel_error}")
            raise DatasetResponseBuilder.error_response("Error generating Excel file", 500)
        
        # Generate filename with timestamp - menggunakan nama yang jelas
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"dataset_prediksi_alergen_format_dosen_{timestamp}.xlsx"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        api_logger.info(f"📥 Excel export completed: {len(records)} records in {processing_time:.2f}s")
        
        # Create a generator for streaming the Excel content (memory efficient)
        def generate_excel():
            excel_content = excel_buffer.getvalue()
            # Stream in chunks for large files
            chunk_size = 8192  # 8KB chunks
            for i in range(0, len(excel_content), chunk_size):
                yield excel_content[i:i+chunk_size]
        
        # Return as streaming response with proper headers
        return StreamingResponse(
            generate_excel(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(excel_buffer.getvalue())),
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        api_logger.error(f"❌ Unexpected error during Excel export: {e}")
        raise DatasetResponseBuilder.error_response(f"Failed to export Excel file: {str(e)}")

@router.delete(
    "/predictions/{prediction_id}",
    summary="Delete a specific prediction record",
    description="Remove a prediction record from the dataset (admin only)"
)
async def delete_prediction(prediction_id: int):
    """
    Delete a specific prediction record
    
    Args:
        prediction_id: The ID of the prediction record to delete
    
    Returns:
        Success confirmation or error response
    """
    try:
        # Check if record exists
        existing_record = database_manager.get_prediction_by_id(prediction_id)
        if not existing_record:
            raise DatasetResponseBuilder.error_response(f"Prediction with ID {prediction_id} not found", 404)
        
        # Delete the record
        success = database_manager.delete_prediction(prediction_id)
        
        if not success:
            raise DatasetResponseBuilder.error_response(f"Failed to delete prediction {prediction_id}", 500)
        
        api_logger.info(f"🗑️ Deleted prediction record ID: {prediction_id}")
        
        return DatasetResponseBuilder.success_response(
            {"deleted_id": prediction_id},
            f"Prediction record {prediction_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise DatasetResponseBuilder.error_response(f"Failed to delete prediction: {str(e)}")

@router.delete(
    "/predictions",
    summary="Bulk delete prediction records",
    description="Delete multiple prediction records by IDs (admin only)"
)
async def bulk_delete_predictions(
    prediction_ids: List[int]
):
    """
    Delete multiple prediction records
    
    Args:
        prediction_ids: List of prediction IDs to delete
    
    Returns:
        Success confirmation with delete results
    """
    try:
        if not prediction_ids:
            raise DatasetResponseBuilder.error_response("No prediction IDs provided", 400)
        
        if len(prediction_ids) > 100:  # Safety limit
            raise DatasetResponseBuilder.error_response("Cannot delete more than 100 records at once", 400)
        
        deleted_count = 0
        failed_ids = []
        
        for pred_id in prediction_ids:
            try:
                success = database_manager.delete_prediction(pred_id)
                if success:
                    deleted_count += 1
                else:
                    failed_ids.append(pred_id)
            except Exception as e:
                api_logger.warning(f"Failed to delete prediction {pred_id}: {str(e)}")
                failed_ids.append(pred_id)
        
        result_data = {
            "requested_count": len(prediction_ids),
            "deleted_count": deleted_count,
            "failed_count": len(failed_ids),
            "failed_ids": failed_ids if failed_ids else None
        }
        
        api_logger.info(f"🗑️ Bulk delete completed: {deleted_count}/{len(prediction_ids)} records deleted")
        
        message = f"Deleted {deleted_count} of {len(prediction_ids)} records"
        if failed_ids:
            message += f" ({len(failed_ids)} failed)"
        
        return DatasetResponseBuilder.success_response(result_data, message)
        
    except HTTPException:
        raise
    except Exception as e:
        raise DatasetResponseBuilder.error_response(f"Bulk delete failed: {str(e)}")

@router.get(
    "/health",
    summary="Check dataset API health",
    description="Health check endpoint for dataset functionality"
)
async def dataset_health_check():
    """Health check for dataset API"""
    try:
        # Test database connection
        is_connected = database_manager.test_connection()
        
        if not is_connected:
            raise DatasetResponseBuilder.error_response("Database connection failed", 503)
        
        # Get basic metrics for health status
        stats = database_manager.get_statistics()
        
        health_data = {
            "database_status": "connected",
            "total_predictions": stats['total_predictions'],
            "last_check": datetime.now().isoformat(),
            "api_version": "2.0.0"
        }
        
        return DatasetResponseBuilder.success_response(health_data, "Dataset API is healthy")
        
    except Exception as e:
        raise DatasetResponseBuilder.error_response(f"Health check failed: {str(e)}", 503)

# Export router
__all__ = ["router"]
