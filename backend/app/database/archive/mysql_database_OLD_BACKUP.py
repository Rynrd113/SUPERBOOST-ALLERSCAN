import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pymysql
from pathlib import Path
import json
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from ..core.logger import api_logger

class MySQLAllergenDatabase:
    """
    MySQL Database handler untuk sistem deteksi alergen
    Menyimpan hasil testing dan dataset dengan hasil deteksi
    """
    
    def __init__(self):
        """
        Initialize MySQL database connection
        """
        # Database configuration for XAMPP
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('MYSQL_PORT', 3306))
        self.username = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')  # Default XAMPP password is empty
        self.database = os.getenv('MYSQL_DATABASE', 'allerscan_db')
        
        # Create database URL
        self.database_url = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}"
        self.database_url_with_db = f"{self.database_url}/{self.database}"
        
        # Create engine and session
        self.engine = None
        self.SessionLocal = None
        
        self.init_database()
    
    def init_database(self):
        """
        Inisialisasi database dan tabel MySQL
        """
        try:
            # First create database if not exists
            temp_engine = create_engine(self.database_url)
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database}"))
                conn.commit()
                api_logger.info(f"✅ Database '{self.database}' created/verified")
            
            # Now connect to the specific database
            self.engine = create_engine(
                self.database_url_with_db,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False  # Set to True for SQL debugging
            )
            
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables
            self._create_tables()
            api_logger.info("✅ MySQL database initialized successfully")
            
        except Exception as e:
            api_logger.error(f"❌ Failed to initialize MySQL database: {e}")
            raise
    
    def _create_tables(self):
        """
        Membuat tabel-tabel yang diperlukan
        """
        with self.engine.connect() as conn:
            # Tabel untuk dataset dengan hasil deteksi
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS dataset_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama_produk VARCHAR(255) NOT NULL,
                    bahan_utama TEXT,
                    pemanis TEXT,
                    lemak_minyak TEXT,
                    penyedap_rasa TEXT,
                    keterangan TEXT,
                    alergen_actual TEXT,
                    alergen_predicted TEXT,
                    confidence DECIMAL(5,4),
                    hasil_deteksi VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_nama_produk (nama_produk),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Tabel untuk hasil testing form
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS form_test_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama_produk VARCHAR(255) NOT NULL,
                    ingredients TEXT NOT NULL,
                    alergen_detected TEXT,
                    confidence DECIMAL(5,4),
                    detailed_results JSON,
                    total_allergens INT DEFAULT 0,
                    test_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    INDEX idx_nama_produk (nama_produk),
                    INDEX idx_test_timestamp (test_timestamp),
                    INDEX idx_confidence (confidence),
                    INDEX idx_total_allergens (total_allergens)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Tabel untuk tracking model performance
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model_type VARCHAR(100) NOT NULL,
                    accuracy DECIMAL(5,4),
                    f1_macro DECIMAL(5,4),
                    f1_micro DECIMAL(5,4),
                    validation_method VARCHAR(100),
                    train_samples INT,
                    test_samples INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_model_type (model_type),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            conn.commit()
            api_logger.info("✅ All MySQL tables created successfully")
    
    def _parse_ingredients_smart(self, ingredients_text: str) -> dict:
        """
        Parse ingredients text dari form user dan kategorikan secara cerdas
        berdasarkan keyword yang umum ditemukan
        
        Args:
            ingredients_text: String bahan-bahan dari user
            
        Returns:
            Dict dengan kategori bahan yang sudah diparsing
        """
        if not ingredients_text:
            return {
                'bahan_utama': 'Tidak Dicantumkan',
                'pemanis': 'Tidak Ada',
                'lemak_minyak': 'Tidak Ada', 
                'penyedap_rasa': 'Tidak Ada'
            }
        
        # Normalize input - lowercase dan split by common separators
        ingredients_lower = ingredients_text.lower()
        ingredients_list = [item.strip() for item in ingredients_lower.replace(',', ' ').replace(';', ' ').split()]
        
        # Define keyword mappings berdasarkan analisis dataset Excel asli
        pemanis_keywords = [
            'gula', 'madu', 'sirup', 'pemanis', 'gula_pasir', 'gula_merah', 'gula_aren', 
            'stevia', 'sakarin', 'aspartam', 'sukrosa', 'fruktosa', 'laktosa',
            'karamel', 'marshmallow', 'molase'
        ]
        
        lemak_keywords = [
            'minyak', 'mentega', 'butter', 'margarin', 'lemak', 'santan', 'krim',
            'olive', 'zaitun', 'sawit', 'kelapa', 'sayur', 'wijen', 'kacang_tanah',
            'samin', 'ghee', 'shortening', 'lard'
        ]
        
        penyedap_keywords = [
            'garam', 'lada', 'merica', 'bumbu', 'rempah', 'bawang', 'seledri',
            'parsley', 'oregano', 'basil', 'thyme', 'rosemary', 'paprika',
            'kunyit', 'jahe', 'kencur', 'lengkuas', 'ketumbar', 'jintan',
            'penyedap', 'msg', 'vetsin', 'kecap', 'saus', 'cuka', 'vanili',
            'ekstrak', 'essence', 'tepung', 'keju', 'parmesan', 'cheddar'
        ]
        
        # Parse dan kategorikan
        found_pemanis = []
        found_lemak = []
        found_penyedap = []
        found_utama = []
        
        for ingredient in ingredients_list:
            # Check pemanis
            if any(keyword in ingredient for keyword in pemanis_keywords):
                found_pemanis.append(ingredient)
            # Check lemak/minyak  
            elif any(keyword in ingredient for keyword in lemak_keywords):
                found_lemak.append(ingredient)
            # Check penyedap rasa
            elif any(keyword in ingredient for keyword in penyedap_keywords):
                found_penyedap.append(ingredient)
            # Default ke bahan utama
            else:
                found_utama.append(ingredient)
        
        # Build result dengan fallback
        result = {
            'bahan_utama': ', '.join(found_utama) if found_utama else ingredients_text,
            'pemanis': ', '.join(found_pemanis) if found_pemanis else 'Tidak Ada',
            'lemak_minyak': ', '.join(found_lemak) if found_lemak else 'Tidak Ada',
            'penyedap_rasa': ', '.join(found_penyedap) if found_penyedap else 'Tidak Ada'
        }
        
        # Jika semua kategori kosong, masukkan semua ke bahan utama
        if all(v == 'Tidak Ada' for k, v in result.items() if k != 'bahan_utama'):
            result['bahan_utama'] = ingredients_text
        
        return result
    
    def get_session(self):
        """
        Get database session
        """
        return self.SessionLocal()
    
    def save_form_result(self, result_data: Dict) -> int:
        """
        Simpan hasil testing dari form ke database
        Sekarang menyimpan ke kedua tabel: form_test_results dan dataset_results
        
        Args:
            result_data: Dictionary dengan data hasil testing
            
        Returns:
            ID record yang tersimpan
        """
        try:
            with self.engine.connect() as conn:
                # 1. Save to form_test_results (existing behavior)
                form_result = conn.execute(text("""
                    INSERT INTO form_test_results 
                    (nama_produk, ingredients, alergen_detected, confidence, 
                     detailed_results, total_allergens, ip_address, user_agent)
                    VALUES (:nama_produk, :ingredients, :alergen_detected, :confidence, 
                            :detailed_results, :total_allergens, :ip_address, :user_agent)
                """), {
                    'nama_produk': result_data.get('productName', ''),
                    'ingredients': result_data.get('ingredients', ''),
                    'alergen_detected': result_data.get('allergen', ''),
                    'confidence': result_data.get('confidence', 0.0),
                    'detailed_results': json.dumps(result_data.get('detailedResults', [])),
                    'total_allergens': result_data.get('totalAllergens', 0),
                    'ip_address': result_data.get('ip_address', ''),
                    'user_agent': result_data.get('user_agent', '')
                })
                
                form_record_id = form_result.lastrowid
                
                # 2. ALSO save to dataset_results (unified view)
                # Parse ingredients to fit dataset structure
                ingredients_text = result_data.get('ingredients', '')
                product_name = result_data.get('productName', 'User Input')
                
                # Smart parsing of ingredients to categorize them
                parsed_ingredients = self._parse_ingredients_smart(ingredients_text)
                
                dataset_result = conn.execute(text("""
                    INSERT INTO dataset_results 
                    (nama_produk, bahan_utama, pemanis, lemak_minyak, penyedap_rasa, 
                     keterangan, alergen_actual, alergen_predicted, confidence, hasil_deteksi)
                    VALUES (:nama_produk, :bahan_utama, :pemanis, :lemak_minyak, :penyedap_rasa,
                            :keterangan, :alergen_actual, :alergen_predicted, :confidence, :hasil_deteksi)
                """), {
                    'nama_produk': product_name,
                    'bahan_utama': parsed_ingredients['bahan_utama'],
                    'pemanis': parsed_ingredients['pemanis'],
                    'lemak_minyak': parsed_ingredients['lemak_minyak'],
                    'penyedap_rasa': parsed_ingredients['penyedap_rasa'], 
                    'keterangan': f'Data input pengguna via form - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    'alergen_actual': 'Unknown',  # User input doesn't have actual allergen info
                    'alergen_predicted': 'tidak terdeteksi' if result_data.get('totalAllergens', 0) == 0 else result_data.get('allergen', 'tidak terdeteksi'),
                    'confidence': result_data.get('confidence', 0.0),
                    'hasil_deteksi': 'Detected' if result_data.get('totalAllergens', 0) > 0 else 'Not Detected'
                })
                
                conn.commit()
                
                api_logger.info(f"✅ Form result saved to both tables. Form ID: {form_record_id}")
                return form_record_id
                
        except Exception as e:
            api_logger.error(f"❌ Error saving form result: {e}")
            raise
    
    def _parse_ingredients_smart(self, ingredients_text: str) -> Dict[str, str]:
        """
        Smart parsing of ingredients text into categories
        """
        if not ingredients_text:
            return {
                'bahan_utama': 'tidak ada',
                'pemanis': 'tidak ada',
                'lemak_minyak': 'tidak ada',
                'penyedap_rasa': 'tidak ada'
            }
        
        # Simple keyword-based categorization
        ingredients_lower = ingredients_text.lower()
        
        # Detect main ingredients
        main_ingredients = []
        sweeteners = []
        fats_oils = []
        flavorings = []
        
        # Keywords for categorization
        sweetener_keywords = ['gula', 'madu', 'sirup', 'pemanis', 'sukrosa', 'fruktosa', 'aspartam']
        fat_oil_keywords = ['minyak', 'mentega', 'lemak', 'margarin', 'butter', 'oil', 'coconut', 'kelapa']
        flavoring_keywords = ['vanilla', 'essence', 'extract', 'rasa', 'aroma', 'penyedap', 'msg', 'garam', 'merica']
        
        words = ingredients_lower.replace(',', ' ').split()
        
        for word in words:
            if any(keyword in word for keyword in sweetener_keywords):
                sweeteners.append(word)
            elif any(keyword in word for keyword in fat_oil_keywords):
                fats_oils.append(word)
            elif any(keyword in word for keyword in flavoring_keywords):
                flavorings.append(word)
            else:
                main_ingredients.append(word)
        
        return {
            'bahan_utama': ', '.join(main_ingredients[:3]) if main_ingredients else ingredients_text[:50],
            'pemanis': ', '.join(sweeteners[:2]) if sweeteners else 'tidak ada',
            'lemak_minyak': ', '.join(fats_oils[:2]) if fats_oils else 'tidak ada', 
            'penyedap_rasa': ', '.join(flavorings[:2]) if flavorings else 'tidak ada'
        }
    
    # REMOVED: load_dataset_from_excel and load_dataset_with_predictions methods
    # Reason: Excel dataset is only for model training, not for displaying in frontend
    # The dataset page should only show results from user form predictions
    
    def get_dataset_with_results(self, limit: int = 10) -> List[Dict]:
        """
        Ambil dataset dengan hasil deteksi
        
        Args:
            limit: Maksimal records yang diambil
            
        Returns:
            List of dictionaries dengan data dataset dan hasil
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT ROW_NUMBER() OVER (ORDER BY created_at ASC) as display_id,
                           id, nama_produk, bahan_utama, pemanis, lemak_minyak, penyedap_rasa,
                           keterangan, alergen_actual, alergen_predicted, confidence, hasil_deteksi, created_at
                    FROM dataset_results 
                    ORDER BY created_at ASC  
                    LIMIT :limit
                """), {'limit': limit})
                
                results = []
                for row in result:
                    results.append({
                        'display_id': row[0],  # Sequential number starting from 1
                        'id': row[1],          # Keep original database ID
                        'nama_produk': row[2],
                        'bahan_utama': row[3],
                        'pemanis': row[4],
                        'lemak_minyak': row[5], 
                        'penyedap_rasa': row[6],
                        'keterangan': row[7],
                        'alergen_actual': row[8],
                        'alergen_predicted': row[9],
                        'confidence_score': float(row[10]) if row[10] else None,
                        'hasil_deteksi': row[11],
                        'created_at': row[12].isoformat() if row[12] else None
                    })
                
                api_logger.info(f"📊 Retrieved {len(results)} dataset records")
                return results
                
        except Exception as e:
            api_logger.error(f"❌ Error getting dataset results: {e}")
            raise
    
    def get_form_results(self, limit: int = 50) -> List[Dict]:
        """
        Ambil hasil testing dari form
        
        Args:
            limit: Maksimal records yang diambil
            
        Returns:
            List of dictionaries dengan hasil form testing
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT ROW_NUMBER() OVER (ORDER BY test_timestamp DESC) as display_id,
                           id, nama_produk, ingredients, alergen_detected, 
                           confidence, total_allergens, test_timestamp
                    FROM form_test_results 
                    ORDER BY test_timestamp DESC 
                    LIMIT :limit
                """), {'limit': limit})
                
                results = []
                for row in result:
                    results.append({
                        'display_id': row[0],  # Sequential number starting from 1
                        'id': row[1],          # Keep original database ID for referencing
                        'nama_produk': row[2],
                        'ingredients': row[3],
                        'alergen_detected': row[4],
                        'confidence': float(row[5]) if row[5] else None,
                        'total_allergens': row[6],
                        'test_timestamp': row[7].isoformat() if row[7] else None
                    })
                
                api_logger.info(f"📊 Retrieved {len(results)} form results")
                return results
                
        except Exception as e:
            api_logger.error(f"❌ Error getting form results: {e}")
            raise
    
    def save_model_performance(self, performance_data: Dict) -> int:
        """
        Simpan data performance model
        
        Args:
            performance_data: Dictionary dengan data performance
            
        Returns:
            ID record yang tersimpan
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO model_performance 
                    (model_type, accuracy, f1_macro, f1_micro, validation_method,
                     train_samples, test_samples)
                    VALUES (:model_type, :accuracy, :f1_macro, :f1_micro, :validation_method,
                            :train_samples, :test_samples)
                """), {
                    'model_type': performance_data.get('model_type', ''),
                    'accuracy': performance_data.get('accuracy', 0.0),
                    'f1_macro': performance_data.get('f1_macro', 0.0),
                    'f1_micro': performance_data.get('f1_micro', 0.0),
                    'validation_method': performance_data.get('validation_method', ''),
                    'train_samples': performance_data.get('train_samples', 0),
                    'test_samples': performance_data.get('test_samples', 0)
                })
                conn.commit()
                
                record_id = result.lastrowid
                api_logger.info(f"✅ Model performance saved with ID: {record_id}")
                return record_id
                
        except Exception as e:
            api_logger.error(f"❌ Error saving model performance: {e}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        Ambil statistik database
        
        Returns:
            Dictionary dengan statistik
        """
        try:
            with self.engine.connect() as conn:
                # Count records
                dataset_count = conn.execute(text("SELECT COUNT(*) FROM dataset_results")).scalar()
                form_count = conn.execute(text("SELECT COUNT(*) FROM form_test_results")).scalar()
                
                # Performance statistics
                avg_confidence = conn.execute(text("""
                    SELECT AVG(confidence) FROM dataset_results 
                    WHERE confidence > 0
                """)).scalar() or 0.0
                
                detection_stats = conn.execute(text("""
                    SELECT 
                        SUM(CASE WHEN hasil_deteksi = 'Detected' THEN 1 ELSE 0 END) as detected,
                        SUM(CASE WHEN hasil_deteksi = 'Not Detected' THEN 1 ELSE 0 END) as not_detected
                    FROM dataset_results
                """)).fetchone()
                
                stats = {
                    'dataset_records': dataset_count,
                    'form_test_records': form_count,
                    'average_confidence': round(float(avg_confidence), 3),
                    'detected_count': detection_stats[0] if detection_stats else 0,
                    'not_detected_count': detection_stats[1] if detection_stats else 0
                }
                
                api_logger.info(f"📊 Database statistics: {stats}")
                return stats
                
        except Exception as e:
            api_logger.error(f"❌ Error getting statistics: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            True if connection successful
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                api_logger.info("✅ MySQL connection test successful")
                return True
        except Exception as e:
            api_logger.error(f"❌ MySQL connection test failed: {e}")
            return False

# Global database instance
db = MySQLAllergenDatabase()
