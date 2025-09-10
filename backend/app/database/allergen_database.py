"""
🗄️ Allergen Database - Clean Architecture Implementation

KONSEP YANG BENAR:
✅ Dataset Excel → Hanya untuk training model ML (TIDAK ditampilkan di website)
✅ Tabel Dataset website → History hasil prediksi dari form user
✅ Flow: User input → ML prediction → Save to database → Display in dataset

Architecture Principles:
✅ DRY (Don't Repeat Yourself)
✅ Single Responsibility Principle
✅ Clean Code & Consistent naming
✅ Reusable Components
✅ Separation of Concerns

@author SuperBoost AllerScan Team
@version 2.0.0 - Clean Architecture
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from ..core.config import settings
from ..core.logger import api_logger

class AllergenDatabaseManager:
    """
    Central database manager following Clean Architecture principles
    
    Responsibilities:
    1. Handle form prediction results (primary data source for website)
    2. Manage database connections with proper pooling
    3. Provide statistics and analytics
    4. Export functionality for admin users
    
    Note: Excel dataset is NOT handled here - it's only for ML model training
    """
    
    def __init__(self):
        """Initialize database connection with optimized settings"""
        self.engine = None
        self.db_available = False
        try:
            self._initialize_connection()
            self._create_tables()
            self.db_available = True
        except Exception as e:
            api_logger.warning(f"⚠️ Database tidak tersedia, menggunakan mode fallback: {e}")
            self.db_available = False
    
    def _initialize_connection(self) -> None:
        """Setup MySQL connection with production-ready configuration"""
        try:
            # Database configuration
            host = os.getenv('MYSQL_HOST', 'localhost')
            port = int(os.getenv('MYSQL_PORT', 3306))
            username = os.getenv('MYSQL_USER', 'root')
            password = os.getenv('MYSQL_PASSWORD', '')
            database_name = os.getenv('MYSQL_DATABASE', 'allerscan_db')
            
            # Connection URLs
            base_url = f"mysql+pymysql://{username}:{password}@{host}:{port}"
            full_url = f"{base_url}/{database_name}"
            
            # Ensure database exists
            temp_engine = create_engine(base_url)
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
                conn.commit()
            
            # Create main engine with connection pooling
            self.engine = create_engine(
                full_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            api_logger.info(f"✅ Database connection established: {host}:{port}/{database_name}")
            
        except Exception as e:
            api_logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def _create_tables(self) -> None:
        """Create necessary tables with proper indexing - using existing migrated tables"""
        with self.engine.connect() as conn:
            # Use existing dataset_results table (migrated from SQLite)
            # This is our PRIMARY data source for the website
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS dataset_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    bahan_utama TEXT,
                    pemanis VARCHAR(255) DEFAULT 'Tidak Ada',
                    lemak_minyak VARCHAR(255) DEFAULT 'Tidak Ada',
                    penyedap_rasa VARCHAR(255) DEFAULT 'Tidak Ada',
                    ingredients_input TEXT NOT NULL,
                    predicted_allergens TEXT,
                    allergen_count INT DEFAULT 0,
                    confidence_score DECIMAL(5,4) DEFAULT 0.0000,
                    risk_level ENUM('none', 'low', 'medium', 'high') DEFAULT 'none',
                    processing_time_ms DECIMAL(8,2) DEFAULT 0.00,
                    model_version VARCHAR(100) DEFAULT 'SVM+AdaBoost',
                    keterangan VARCHAR(500) DEFAULT 'Form input pengguna',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_ip VARCHAR(45),
                    user_agent TEXT,
                    
                    INDEX idx_created_at (created_at),
                    INDEX idx_product_name (product_name),
                    INDEX idx_allergen_count (allergen_count),
                    INDEX idx_confidence (confidence_score),
                    INDEX idx_risk_level (risk_level)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Form test results table  
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS form_test_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_name VARCHAR(255),
                    ingredients TEXT,
                    expected_result TEXT,
                    actual_result TEXT,
                    confidence DECIMAL(5,4),
                    status ENUM('passed', 'failed') DEFAULT 'passed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    INDEX idx_test_name (test_name),
                    INDEX idx_status (status),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Table for model performance tracking
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_type VARCHAR(100) NOT NULL,
                    accuracy DECIMAL(5,4),
                    cross_validation_score DECIMAL(5,4),
                    training_samples INT,
                    test_samples INT,
                    feature_count INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    INDEX idx_model_type (model_type),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            conn.commit()
            api_logger.info("✅ Database tables created/verified successfully")
    
    def save_prediction_result(self, prediction_data: dict) -> int:
        """
        Save prediction result to database with fallback
        
        Args:
            prediction_data: Dictionary containing prediction results
            
        Returns:
            ID of saved record (0 if database unavailable)
        """
        if not self.db_available:
            api_logger.info("📝 Database tidak tersedia, skip saving prediction")
            return 0
            
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO dataset_results 
                    (product_name, bahan_utama, pemanis, lemak_minyak, penyedap_rasa,
                     ingredients_input, predicted_allergens, allergen_count,
                     confidence_score, risk_level, processing_time_ms, model_version,
                     keterangan, user_ip, user_agent)
                    VALUES (:product_name, :bahan_utama, :pemanis, :lemak_minyak, :penyedap_rasa,
                            :ingredients_input, :predicted_allergens, :allergen_count, 
                            :confidence_score, :risk_level, :processing_time_ms, 
                            :model_version, :keterangan, :user_ip, :user_agent)
                """), {
                    'product_name': prediction_data.get('productName', ''),
                    'bahan_utama': prediction_data.get('bahan_utama', ''),
                    'pemanis': prediction_data.get('pemanis', 'Tidak Ada'),
                    'lemak_minyak': prediction_data.get('lemak_minyak', 'Tidak Ada'), 
                    'penyedap_rasa': prediction_data.get('penyedap_rasa', 'Tidak Ada'),
                    'ingredients_input': prediction_data.get('ingredients', ''),
                    'predicted_allergens': prediction_data.get('allergens', 'tidak terdeteksi'),
                    'allergen_count': prediction_data.get('allergen_count', 0),
                    'confidence_score': prediction_data.get('confidence', 0.0),
                    'risk_level': prediction_data.get('risk_level', 'none'),
                    'processing_time_ms': prediction_data.get('processing_time_ms', 0.0),
                    'model_version': prediction_data.get('model_version', 'SVM+AdaBoost'),
                    'keterangan': f"Form input: {prediction_data.get('productName', '')}",
                    'user_ip': prediction_data.get('user_ip', ''),
                    'user_agent': prediction_data.get('user_agent', '')
                })
                
                conn.commit()
                record_id = result.lastrowid
                api_logger.info(f"✅ Prediction saved to database with ID: {record_id}")
                return record_id
                
        except Exception as e:
            api_logger.error(f"❌ Error saving prediction: {e}")
            return 0
    
    def get_prediction_history(self, limit: int = 100, offset: int = 0) -> Dict:
        """
        Get paginated prediction history for dataset display with total count
        
        Args:
            limit: Maximum number of records to retrieve
            offset: Number of records to skip
            
        Returns:
            Dictionary with records list and pagination metadata
        """
        if not self.db_available:
            return {
                'records': [],
                'total_count': 0,
                'message': 'Database tidak tersedia'
            }
            
        try:
            with self.engine.connect() as conn:
                # Get total count for pagination
                total_count = conn.execute(text(
                    "SELECT COUNT(*) FROM dataset_results"
                )).scalar()
                
                # Get paginated records
                result = conn.execute(text("""
                    SELECT 
                        (ROW_NUMBER() OVER (ORDER BY created_at DESC) + :offset) as display_id,
                        id, product_name, bahan_utama, pemanis, lemak_minyak, penyedap_rasa,
                        ingredients_input, predicted_allergens, allergen_count, 
                        confidence_score, risk_level, processing_time_ms, model_version, 
                        keterangan, created_at
                    FROM dataset_results 
                    ORDER BY created_at DESC 
                    LIMIT :limit OFFSET :offset
                """), {'limit': limit, 'offset': offset})
                
                records = []
                for row in result:
                    records.append({
                        'display_id': row[0],
                        'id': row[1], 
                        'product_name': row[2],  # nama produk
                        'nama_produk': row[2],   # alias untuk konsistensi
                        'bahan_utama': row[3],
                        'pemanis': row[4],
                        'lemak_minyak': row[5], 
                        'penyedap_rasa': row[6],
                        'ingredients': row[7],   # ingredients input
                        'ingredients_input': row[7],  # alias
                        'detected_allergens': row[8],  # predicted allergens
                        'predicted_allergens': row[8],  # alias
                        'allergen_count': row[9],
                        'confidence_score': float(row[10]) if row[10] else 0.0,
                        'risk_level': row[11],
                        'processing_time': float(row[12]) if row[12] else 0.0,
                        'model_version': row[13],
                        'keterangan': row[14],
                        'created_at': row[15].isoformat() if row[15] else None,
                        'detection_status': 'Terdeteksi' if row[9] > 0 else 'Tidak Terdeteksi'
                    })
                
                # Calculate pagination metadata
                total_pages = (total_count + limit - 1) // limit  # Ceiling division
                has_more = offset + limit < total_count
                
                pagination_data = {
                    'records': records,
                    'pagination': {
                        'total_items': total_count,
                        'total_pages': total_pages,
                        'current_page': (offset // limit) + 1,
                        'items_per_page': limit,
                        'has_more': has_more,
                        'has_previous': offset > 0,
                        'showing_from': offset + 1 if records else 0,
                        'showing_to': offset + len(records)
                    }
                }
                
                api_logger.info(f"📊 Retrieved {len(records)}/{total_count} records (page {pagination_data['pagination']['current_page']}/{total_pages})")
                return pagination_data
                
        except Exception as e:
            api_logger.error(f"❌ Error retrieving prediction history: {e}")
            return {
                'records': [],
                'total_count': 0,
                'message': f'Database error: {e}'
            }
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics for dashboard with dynamic model accuracy"""
        if not self.db_available:
            return {
                'total_predictions': 0,
                'detected_count': 0,
                'not_detected_count': 0,
                'detection_rate': 0.0,
                'average_confidence': 0.0,
                'average_processing_time': '<500ms',
                'message': 'Database tidak tersedia'
            }
            
        try:
            with self.engine.connect() as conn:
                # Basic counts
                total_predictions = conn.execute(text(
                    "SELECT COUNT(*) FROM dataset_results"
                )).scalar()
                
                detected_count = conn.execute(text(
                    "SELECT COUNT(*) FROM dataset_results WHERE allergen_count > 0"
                )).scalar()
                
                # Average metrics
                avg_confidence = conn.execute(text(
                    "SELECT AVG(confidence_score) FROM dataset_results WHERE confidence_score > 0"
                )).scalar() or 0.0
                
                avg_processing_time = conn.execute(text(
                    "SELECT AVG(processing_time_ms) FROM dataset_results"
                )).scalar() or 0.0
                
                # Get latest model performance from model_performance table
                latest_model_accuracy = conn.execute(text("""
                    SELECT cross_validation_score 
                    FROM model_performance 
                    WHERE model_type = 'SVM+AdaBoost' 
                    ORDER BY created_at DESC 
                    LIMIT 1
                """)).scalar()
                
                # Risk level distribution
                risk_distribution = conn.execute(text("""
                    SELECT risk_level, COUNT(*) as count
                    FROM dataset_results 
                    GROUP BY risk_level
                """)).fetchall()
                
                # Format processing time untuk display
                processing_time_display = f"<{int(avg_processing_time)}ms" if avg_processing_time < 1000 else f"{avg_processing_time/1000:.1f}s"
                
                # Use dynamic model accuracy if available, otherwise fallback
                model_accuracy = f"{latest_model_accuracy * 100:.1f}%" if latest_model_accuracy else "93.7%"
                
                stats = {
                    'total_predictions': total_predictions,
                    'detected_count': detected_count,
                    'not_detected_count': total_predictions - detected_count,
                    'detection_rate': round((detected_count / total_predictions * 100), 2) if total_predictions > 0 else 0.0,
                    'average_confidence': round(float(avg_confidence) * 100, 2),
                    'average_processing_time': processing_time_display,
                    'risk_distribution': {row[0]: row[1] for row in risk_distribution},
                    'model_info': {
                        'algorithm': 'SVM + AdaBoost',
                        'accuracy': model_accuracy,  # Dynamic accuracy
                        'cross_validation': 'K-Fold (k=10)',
                        'encoding': 'One-Hot Encoding'
                    }
                }
                
                api_logger.info(f"📊 Statistics calculated successfully - Accuracy: {model_accuracy}")
                return stats
                
        except Exception as e:
            api_logger.error(f"❌ Error calculating statistics: {e}")
            raise
    
    def save_model_performance(self, performance_data: Dict) -> int:
        """Save model performance metrics"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO model_performance 
                    (model_type, accuracy, cross_validation_score, training_samples,
                     test_samples, feature_count)
                    VALUES (:model_type, :accuracy, :cv_score, :train_samples,
                            :test_samples, :feature_count)
                """), {
                    'model_type': performance_data.get('model_type', 'SVM+AdaBoost'),
                    'accuracy': performance_data.get('accuracy', 0.0),
                    'cv_score': performance_data.get('cv_score', 0.0),
                    'train_samples': performance_data.get('train_samples', 0),
                    'test_samples': performance_data.get('test_samples', 0),
                    'feature_count': performance_data.get('feature_count', 0)
                })
                
                conn.commit()
                record_id = result.lastrowid
                
                api_logger.info(f"✅ Model performance saved with ID: {record_id}")
                return record_id
                
        except Exception as e:
            api_logger.error(f"❌ Error saving model performance: {e}")
            raise
    
    def get_top_allergens(self, limit: int = 6) -> List[Dict]:
        """Get top allergens from all predictions for chart display"""
        try:
            with self.engine.connect() as conn:
                # Get all allergens from predictions
                result = conn.execute(text("""
                    SELECT predicted_allergens 
                    FROM dataset_results 
                    WHERE predicted_allergens IS NOT NULL 
                    AND predicted_allergens != 'tidak terdeteksi'
                    AND allergen_count > 0
                """))
                
                allergen_count = {}
                for row in result:
                    if row[0]:
                        # Split allergens and count each one
                        allergens = [a.strip() for a in row[0].split(',') if a.strip()]
                        for allergen in allergens:
                            allergen_count[allergen] = allergen_count.get(allergen, 0) + 1
                
                # Sort by count and get top allergens
                top_allergens = sorted(allergen_count.items(), key=lambda x: x[1], reverse=True)[:limit]
                
                return [{"name": name, "count": count} for name, count in top_allergens]
                
        except Exception as e:
            api_logger.error(f"❌ Error getting top allergens: {e}")
            return []
    
    def get_prediction_by_id(self, prediction_id: int) -> Optional[Dict]:
        """
        Get a specific prediction record by ID
        
        Args:
            prediction_id: The ID of the prediction record
            
        Returns:
            Dict with prediction data or None if not found
        """
        try:
            with self.engine.connect() as conn:
                query = """
                SELECT 
                    id, product_name, ingredients_input, predicted_allergens, 
                    allergen_count, confidence_score, risk_level,
                    processing_time_ms, model_version, created_at
                FROM dataset_results 
                WHERE id = :prediction_id
                """
                
                result = conn.execute(text(query), {"prediction_id": prediction_id}).fetchone()
                
                if not result:
                    return None
                
                # Convert to dictionary
                record = {
                    "id": result[0],
                    "product_name": result[1],
                    "ingredients_input": result[2],
                    "predicted_allergens": result[3],
                    "allergen_count": result[4],
                    "confidence_score": float(result[5]) if result[5] else 0.0,
                    "risk_level": result[6],
                    "processing_time_ms": float(result[7]) if result[7] else 0.0,
                    "model_version": result[8],
                    "created_at": result[9].isoformat() if result[9] else None
                }
                
                api_logger.info(f"📄 Retrieved prediction record ID: {prediction_id}")
                return record
                
        except Exception as e:
            api_logger.error(f"❌ Error getting prediction by ID {prediction_id}: {e}")
            return None
    
    def delete_prediction(self, prediction_id: int) -> bool:
        """
        Delete a specific prediction record
        
        Args:
            prediction_id: The ID of the prediction record to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                # Check if record exists first (use dataset_results table)
                check_query = "SELECT COUNT(*) as count FROM dataset_results WHERE id = :prediction_id"
                count_result = conn.execute(text(check_query), {"prediction_id": prediction_id}).fetchone()
                
                if count_result.count == 0:
                    api_logger.warning(f"⚠️ Prediction ID {prediction_id} not found for deletion")
                    return False
                
                # Delete the record (use dataset_results table)
                delete_query = "DELETE FROM dataset_results WHERE id = :prediction_id"
                result = conn.execute(text(delete_query), {"prediction_id": prediction_id})
                conn.commit()
                
                if result.rowcount > 0:
                    api_logger.info(f"🗑️ Successfully deleted prediction ID: {prediction_id}")
                    return True
                else:
                    api_logger.warning(f"⚠️ No rows affected when deleting prediction ID: {prediction_id}")
                    return False
                    
        except Exception as e:
            api_logger.error(f"❌ Error deleting prediction {prediction_id}: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test database connectivity"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            api_logger.error(f"❌ Database connection test failed: {e}")
            return False

# Create global database instance
database_manager = AllergenDatabaseManager()

# Export for backward compatibility
db = database_manager

# Public API exports
__all__ = [
    'AllergenDatabaseManager',
    'database_manager', 
    'db'
]
