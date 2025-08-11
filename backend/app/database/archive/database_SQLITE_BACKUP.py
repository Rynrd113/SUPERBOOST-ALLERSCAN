import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd

class AllergenDatabase:
    """
    Database handler untuk sistem deteksi alergen
    Menyimpan hasil testing dan dataset dengan hasil deteksi
    """
    
    def __init__(self, db_path: str = "allergen_results.db"):
        """
        Initialize database connection
        """
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """
        Inisialisasi tabel database
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabel untuk dataset dengan hasil deteksi
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dataset_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_produk TEXT NOT NULL,
                    bahan_utama TEXT,
                    pemanis TEXT,
                    lemak_minyak TEXT,
                    penyedap_rasa TEXT,
                    keterangan TEXT,
                    alergen_actual TEXT,
                    alergen_predicted TEXT,
                    confidence REAL,
                    hasil_deteksi TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabel untuk hasil testing form
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS form_test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_produk TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    alergen_detected TEXT,
                    confidence REAL,
                    detailed_results TEXT,
                    total_allergens INTEGER,
                    test_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT
                )
            """)
            
            # Tabel untuk tracking model performance
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_type TEXT NOT NULL,
                    accuracy REAL,
                    f1_macro REAL,
                    f1_micro REAL,
                    validation_method TEXT,
                    train_samples INTEGER,
                    test_samples INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def save_form_result(self, result_data: Dict) -> int:
        """
        Simpan hasil testing dari form ke database
        
        Args:
            result_data: Dictionary dengan data hasil testing
            
        Returns:
            ID record yang tersimpan
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO form_test_results 
                (nama_produk, ingredients, alergen_detected, confidence, 
                 detailed_results, total_allergens, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result_data.get('productName', ''),
                result_data.get('ingredients', ''),
                result_data.get('allergen', ''),
                result_data.get('confidence', 0.0),
                json.dumps(result_data.get('detailedResults', [])),
                result_data.get('totalAllergens', 0),
                result_data.get('ip_address', ''),
                result_data.get('user_agent', '')
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def load_dataset_from_excel(self, excel_path: str) -> None:
        """
        Load dataset langsung dari Excel file asli dosen dan buat prediksi untuk semua item
        
        Args:
            excel_path: Path ke file Excel dataset asli
        """
        try:
            # Load dataset langsung dari Excel sesuai script dosen
            df = pd.read_excel(excel_path, sheet_name='Dataset')
            print(f"📊 Loading dataset dari Excel dengan {len(df)} items...")
            
            # Import predictor
            from ..models.inference.predictor import AllergenPredictor
            predictor = AllergenPredictor()
            
            if not predictor.is_loaded:
                raise Exception("Failed to load SVM + AdaBoost model")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing data
                cursor.execute("DELETE FROM dataset_results")
                print("🗑️ Cleared existing dataset results")
                
                # Process in batches to improve performance
                batch_size = 10
                processed_count = 0
                
                for i in range(0, len(df), batch_size):
                    batch_df = df.iloc[i:i+batch_size]
                    print(f"🔄 Processing batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1} ({len(batch_df)} items)...")
                    
                    for _, row in batch_df.iterrows():
                        try:
                            # Prepare data sesuai format script dosen
                            ingredients_data = {
                                'Nama Produk Makanan': str(row.get('Nama Produk Makanan', '')),
                                'Bahan Utama': str(row.get('Bahan Utama', '')),
                                'Pemanis': str(row.get('Pemanis', '')),
                                'Lemak/Minyak': str(row.get('Lemak/Minyak', '')),
                                'Penyedap Rasa': str(row.get('Penyedap Rasa', '')),
                                'Alergen': str(row.get('Alergen', ''))
                            }
                            
                            # Make prediction
                            results, metadata = predictor.predict_allergens(
                                ingredients_data=ingredients_data,
                                confidence_threshold=0.5
                            )
                            
                            predicted_allergens = []
                            confidence_avg = 0.0
                            
                            if results:
                                predicted_allergens = [r.allergen for r in results]
                                confidence_avg = sum(r.confidence for r in results) / len(results)
                                
                            alergen_predicted = ', '.join(predicted_allergens) if predicted_allergens else 'tidak terdeteksi'
                            hasil_deteksi = 'Detected' if predicted_allergens else 'Not Detected'
                            
                        except Exception as e:
                            print(f"❌ Prediction error for {row.get('Nama Produk Makanan', '')}: {e}")
                            alergen_predicted = 'error'
                            confidence_avg = 0.0
                            hasil_deteksi = 'Error'
                        
                        # Simpan ke database
                        cursor.execute("""
                            INSERT INTO dataset_results 
                            (nama_produk, bahan_utama, pemanis, lemak_minyak, penyedap_rasa, 
                             keterangan, alergen_actual, alergen_predicted, confidence, hasil_deteksi)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get('Nama Produk Makanan', ''),
                            row.get('Bahan Utama', ''),
                            row.get('Pemanis', ''),
                            row.get('Lemak/Minyak', ''),
                            row.get('Penyedap Rasa', ''),
                            row.get('Keterangan', ''),
                            row.get('Alergen', ''),
                            alergen_predicted,
                            confidence_avg,
                            hasil_deteksi
                        ))
                        
                        processed_count += 1
                    
                    # Commit batch and show progress
                    conn.commit()
                    print(f"✅ Processed {processed_count}/{len(df)} items ({(processed_count/len(df)*100):.1f}%)")
                
                print(f"🎉 Dataset dengan {len(df)} items berhasil dimuat ke database dari Excel")
                
        except Exception as e:
            print(f"❌ Error loading dataset dari Excel: {e}")
            raise
    
    def load_dataset_with_predictions(self, csv_path: str) -> None:
        """
        Load dataset dan buat prediksi untuk semua item, simpan ke database
        
        Args:
            csv_path: Path ke file CSV dataset
        """
        try:
            # Load dataset
            df = pd.read_csv(csv_path)
            print(f"📊 Loading dataset with {len(df)} items...")
            
            # Import predictor
            from ..models.inference.predictor import AllergenPredictor
            predictor = AllergenPredictor()
            
            if not predictor.load_models():
                raise Exception("Failed to load ML models")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing data
                cursor.execute("DELETE FROM dataset_results")
                print("🗑️ Cleared existing dataset results")
                
                # Process in batches to improve performance
                batch_size = 10
                processed_count = 0
                
                for i in range(0, len(df), batch_size):
                    batch_df = df.iloc[i:i+batch_size]
                    print(f"🔄 Processing batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1} ({len(batch_df)} items)...")
                    
                    for _, row in batch_df.iterrows():
                        # Buat structured text untuk prediksi
                        ingredients = f"{row.get('Bahan Utama', '')} {row.get('Pemanis', '')} {row.get('Lemak/Minyak', '')} {row.get('Penyedap Rasa', '')}"
                        ingredients = ' '.join(ingredients.split())  # Clean whitespace
                        
                        # Prediksi
                        try:
                            results, metadata = predictor.predict_allergens(ingredients)
                            
                            predicted_allergens = []
                            confidence_avg = 0.0
                            
                            if results:
                                predicted_allergens = [r.allergen for r in results]
                                confidence_avg = sum(r.confidence for r in results) / len(results)
                                
                            alergen_predicted = ', '.join(predicted_allergens) if predicted_allergens else 'tidak terdeteksi'
                            hasil_deteksi = 'Detected' if predicted_allergens else 'Not Detected'
                            
                        except Exception as e:
                            print(f"❌ Prediction error for {row.get('Nama Produk Makanan', '')}: {e}")
                            alergen_predicted = 'error'
                            confidence_avg = 0.0
                            hasil_deteksi = 'Error'
                        
                        # Simpan ke database
                        cursor.execute("""
                            INSERT INTO dataset_results 
                            (nama_produk, bahan_utama, pemanis, lemak_minyak, penyedap_rasa, 
                             keterangan, alergen_actual, alergen_predicted, confidence, hasil_deteksi)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get('Nama Produk Makanan', ''),
                            row.get('Bahan Utama', ''),
                            row.get('Pemanis', ''),
                            row.get('Lemak/Minyak', ''),
                            row.get('Penyedap Rasa', ''),
                            row.get('Keterangan', ''),
                            row.get('Alergen', ''),
                            alergen_predicted,
                            confidence_avg,
                            hasil_deteksi
                        ))
                        
                        processed_count += 1
                    
                    # Commit batch and show progress
                    conn.commit()
                    print(f"✅ Processed {processed_count}/{len(df)} items ({(processed_count/len(df)*100):.1f}%)")
                
                print(f"🎉 Dataset dengan {len(df)} items berhasil dimuat ke database")
                
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            raise
                
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
    
    def get_dataset_with_results(self, limit: int = 10) -> List[Dict]:
        """
        Ambil dataset dengan hasil deteksi
        
        Args:
            limit: Maksimal records yang diambil
            
        Returns:
            List of dictionaries dengan data dataset dan hasil
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, nama_produk, bahan_utama, alergen_actual, 
                       alergen_predicted, confidence, hasil_deteksi, created_at
                FROM dataset_results 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
    
    def get_form_results(self, limit: int = 50) -> List[Dict]:
        """
        Ambil hasil testing dari form
        
        Args:
            limit: Maksimal records yang diambil
            
        Returns:
            List of dictionaries dengan hasil form testing
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, nama_produk, ingredients, alergen_detected, 
                       confidence, total_allergens, test_timestamp
                FROM form_test_results 
                ORDER BY test_timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
    
    def save_model_performance(self, performance_data: Dict) -> int:
        """
        Simpan data performance model
        
        Args:
            performance_data: Dictionary dengan data performance
            
        Returns:
            ID record yang tersimpan
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO model_performance 
                (model_type, accuracy, f1_macro, f1_micro, validation_method,
                 train_samples, test_samples)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                performance_data.get('model_type', ''),
                performance_data.get('accuracy', 0.0),
                performance_data.get('f1_macro', 0.0),
                performance_data.get('f1_micro', 0.0),
                performance_data.get('validation_method', ''),
                performance_data.get('train_samples', 0),
                performance_data.get('test_samples', 0)
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_statistics(self) -> Dict:
        """
        Ambil statistik database
        
        Returns:
            Dictionary dengan statistik
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM dataset_results")
            dataset_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM form_test_results")
            form_count = cursor.fetchone()[0]
            
            # Performance statistics
            cursor.execute("""
                SELECT AVG(confidence) FROM dataset_results 
                WHERE confidence > 0
            """)
            avg_confidence = cursor.fetchone()[0] or 0.0
            
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN hasil_deteksi = 'Detected' THEN 1 ELSE 0 END) as detected,
                    SUM(CASE WHEN hasil_deteksi = 'Not Detected' THEN 1 ELSE 0 END) as not_detected
                FROM dataset_results
            """)
            detection_stats = cursor.fetchone()
            
            return {
                'dataset_records': dataset_count,
                'form_test_records': form_count,
                'average_confidence': round(avg_confidence, 3),
                'detected_count': detection_stats[0] if detection_stats else 0,
                'not_detected_count': detection_stats[1] if detection_stats else 0
            }

# Global database instance
db = AllergenDatabase()
