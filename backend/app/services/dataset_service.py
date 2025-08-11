"""
🔧 Dataset Service Layer - Clean Architecture

Service untuk menangani operasi dataset dengan separation of concerns
Mengikuti prinsip DRY dan Single Responsibility

@author SuperBoost AllerScan Team  
@version 2.0.0
@updated 2025-08-10
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from io import BytesIO

from ..core.logger import api_logger
from ..database.allergen_database import database_manager

class DatasetService:
    """
    Service layer untuk operasi dataset
    
    Responsibilities:
    1. Retrieve prediction history dengan pagination
    2. Calculate statistics dan analytics
    3. Export data ke berbagai format
    4. Data filtering dan sorting
    """
    
    def __init__(self):
        self.db = database_manager
    
    async def get_prediction_history(self, page: int = 1, limit: int = 50, include_stats: bool = True) -> Dict[str, Any]:
        """
        Get paginated prediction history dengan optional statistics
        
        Args:
            page: Page number (1-based)
            limit: Items per page
            include_stats: Include statistics in response
            
        Returns:
            Dictionary dengan predictions dan metadata
        """
        try:
            offset = (page - 1) * limit
            
            # Get predictions dengan pagination metadata (UPDATED)
            result = self.db.get_prediction_history(limit=limit, offset=offset)
            
            response = {
                'success': True,
                'predictions': result['records'],  # Use records from new response format
                'pagination': result['pagination'],  # Use pagination from new response format
                'meta': {
                    'retrieved_at': datetime.now().isoformat(),
                    'data_source': 'user_form_predictions'
                }
            }
            
            # Include statistics jika diminta
            if include_stats:
                response['statistics'] = await self.get_comprehensive_statistics()
            
            api_logger.info(f"📊 Retrieved {len(result['records'])} predictions for page {page}")
            return response
            
        except Exception as e:
            api_logger.error(f"❌ Error getting prediction history: {e}")
            return {
                'success': False,
                'error': str(e),
                'predictions': [],
                'pagination': {
                    'current_page': page,
                    'total_pages': 0,
                    'total_items': 0,
                    'items_per_page': limit,
                    'has_next': False,
                    'has_previous': False
                }
            }
    
    async def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics untuk dashboard
        
        Returns:
            Dictionary dengan berbagai statistik
        """
        try:
            base_stats = self.db.get_statistics()
            
            # Enhanced statistics
            enhanced_stats = {
                **base_stats,
                'data_quality': {
                    'completeness_rate': self._calculate_completeness_rate(base_stats),
                    'confidence_distribution': await self._get_confidence_distribution(),
                    'temporal_distribution': await self._get_temporal_distribution()
                },
                'insights': self._generate_insights(base_stats),
                'generated_at': datetime.now().isoformat()
            }
            
            return enhanced_stats
            
        except Exception as e:
            api_logger.error(f"❌ Error calculating comprehensive statistics: {e}")
            return {'error': str(e)}
    
    async def export_to_excel(self, limit: int = 1000) -> BytesIO:
        """
        Export prediction data to Excel format
        
        Args:
            limit: Maximum number of records to export
            
        Returns:
            BytesIO object dengan Excel data
        """
        try:
            # Get data
            predictions = self.db.get_prediction_history(limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(predictions)
            
            # Clean and format columns
            df = self._format_dataframe_for_export(df)
            
            # Create Excel file
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Dataset Bahan Makanan & Alergen', index=False)
                
                # Add statistics sheet
                stats = await self.get_comprehensive_statistics()
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name='Ringkasan Statistik', index=False)
            
            excel_buffer.seek(0)
            api_logger.info(f"📊 Exported {len(predictions)} records to Excel")
            return excel_buffer
            
        except Exception as e:
            api_logger.error(f"❌ Error exporting to Excel: {e}")
            raise
    
    def _format_dataframe_for_export(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format DataFrame untuk export sesuai format Dataset Dosen"""
        # Format sesuai dataset dosen: nama produk pangan, bahan pokok, pemanis, lemak/minyak, bumbu, alergen, hasil deteksi
        column_mapping = {
            'product_name': 'Nama Produk Pangan',
            'bahan_utama': 'Bahan Pokok',
            'pemanis': 'Pemanis',
            'lemak_minyak': 'Lemak/Minyak',
            'penyedap_rasa': 'Bumbu',
            'ingredients_input': 'Alergen',  # Input ingredients sebagai kolom alergen
            'predicted_allergens': 'Hasil Deteksi',  # Hasil prediksi
            'confidence_score': 'Tingkat Kepercayaan (%)',
            'created_at': 'Tanggal Prediksi'
        }
        
        # Apply column mapping
        df = df.rename(columns=column_mapping)
        
        # Select columns sesuai format dosen + info tambahan penting
        dosen_columns = ['Nama Produk Pangan', 'Bahan Pokok', 'Pemanis', 'Lemak/Minyak', 'Bumbu', 'Alergen', 'Hasil Deteksi']
        extra_columns = ['Tingkat Kepercayaan (%)', 'Tanggal Prediksi']
        
        # Filter available columns
        available_columns = [col for col in dosen_columns + extra_columns if col in df.columns]
        df = df[available_columns]
        
        # Format confidence score as percentage
        if 'Tingkat Kepercayaan (%)' in df.columns:
            df['Tingkat Kepercayaan (%)'] = (df['Tingkat Kepercayaan (%)'] * 100).round(2)
        
        return df
    
    async def _get_total_predictions_count(self) -> int:
        """Get total count of predictions"""
        try:
            # Implementasi tergantung database method
            # Untuk sekarang, estimate dari statistics
            stats = self.db.get_statistics()
            return stats.get('total_predictions', 0)
        except Exception as e:
            api_logger.error(f"❌ Error getting total count: {e}")
            return 0
    
    def _calculate_completeness_rate(self, stats: Dict) -> float:
        """Calculate data completeness rate"""
        total = stats.get('total_predictions', 0)
        if total == 0:
            return 100.0
        
        # Estimate completeness berdasarkan data yang ada
        complete_records = stats.get('detected_count', 0) + stats.get('not_detected_count', 0)
        return round((complete_records / total) * 100, 2)
    
    async def _get_confidence_distribution(self) -> Dict[str, int]:
        """Get confidence score distribution"""
        try:
            # Placeholder - implementasi tergantung database query capabilities
            return {
                'high_confidence': 45,  # >80%
                'medium_confidence': 35,  # 50-80%
                'low_confidence': 20   # <50%
            }
        except Exception as e:
            api_logger.error(f"❌ Error getting confidence distribution: {e}")
            return {}
    
    async def _get_temporal_distribution(self) -> Dict[str, int]:
        """Get temporal distribution of predictions"""
        try:
            # Placeholder - implementasi tergantung database query capabilities
            return {
                'today': 12,
                'this_week': 78,
                'this_month': 234,
                'older': 156
            }
        except Exception as e:
            api_logger.error(f"❌ Error getting temporal distribution: {e}")
            return {}
    
    def _generate_insights(self, stats: Dict) -> List[str]:
        """Generate data insights berdasarkan statistics"""
        insights = []
        
        detection_rate = stats.get('detection_rate', 0)
        total_predictions = stats.get('total_predictions', 0)
        avg_confidence = stats.get('average_confidence', 0)
        
        # Detection rate insight
        if detection_rate > 60:
            insights.append(f"Tingkat deteksi alergen tinggi ({detection_rate}%) - menunjukkan banyak produk mengandung alergen")
        elif detection_rate < 30:
            insights.append(f"Tingkat deteksi alergen rendah ({detection_rate}%) - mayoritas produk aman dari alergen")
        
        # Volume insight
        if total_predictions > 1000:
            insights.append(f"Volume prediksi tinggi ({total_predictions:,} total) menunjukkan sistem aktif digunakan")
        
        # Confidence insight
        if avg_confidence > 80:
            insights.append(f"Model menunjukkan kepercayaan tinggi ({avg_confidence}%) pada prediksi")
        elif avg_confidence < 60:
            insights.append(f"Kepercayaan model rendah ({avg_confidence}%) - perlu evaluasi lebih lanjut")
        
        return insights

# Create singleton instance
dataset_service = DatasetService()

# Export
__all__ = ['DatasetService', 'dataset_service']
