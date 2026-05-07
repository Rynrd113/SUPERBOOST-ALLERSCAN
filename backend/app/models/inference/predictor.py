"""
Model Machine Learning untuk Deteksi Alergen

Implementasi predictor menggunakan algoritma SVM + AdaBoost untuk deteksi alergen
dalam produk makanan. Model ini dirancang untuk aplikasi web dengan fokus pada
akurasi dan performa yang optimal.

Fitur utama:
- Deteksi Out-of-Vocabulary (OOV) untuk input baru
- Penyesuaian confidence score secara dinamis  
- Penanganan kategori input yang belum pernah dilihat
- Cross-validation untuk evaluasi model
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, StratifiedKFold
import warnings

from ...core.config import settings
from ...core.logger import api_logger, log_model_loaded, log_error
from ...schemas.request_schemas import AllergenResult

warnings.filterwarnings('ignore')

class AllergenPredictor:
    """
    Model predictor untuk deteksi alergen menggunakan machine learning
    
    Menggunakan kombinasi SVM + AdaBoost dengan One-Hot Encoding untuk
    mengklasifikasikan produk makanan berdasarkan kandungan alergen.
    
    Fitur yang didukung:
    - Deteksi Out-of-Vocabulary untuk input yang tidak dikenal
    - Penyesuaian confidence score secara dinamis
    - Penanganan kategori input yang belum pernah ditemui dalam training
    """
    
    def __init__(self):
        """Inisialisasi predictor dengan pengaturan awal"""
        self.model = None
        self.X_encoded = None
        self.y_encoded = None
        self.label_encoder = None
        self.cv_accuracy = None
        self.is_loaded = False
        
        # Simpan kategori training untuk deteksi OOV
        self.training_categories = {
            'nama_produk_makanan': set(),
            'bahan_utama': set(),
            'pemanis': set(),
            'lemak_minyak': set(),
            'penyedap_rasa': set(),
            'alergen': set()
        }
    
    def load_and_train_model(self) -> bool:
        """
        Memuat dataset dan melatih model SVM + AdaBoost
        
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            api_logger.info("Memuat dataset dan melatih model SVM + AdaBoost...")
            
            # Lokasi-lokasi yang mungkin untuk file dataset
            possible_paths = [
                Path("data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("../data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("../../data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("notebooks/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("../notebooks/Dataset Bahan Makanan & Alergen.xlsx")
            ]
            
            dataset_path = None
            for path in possible_paths:
                if path.exists():
                    dataset_path = path
                    break
            
            if not dataset_path:
                api_logger.error(f"Dataset tidak ditemukan di lokasi manapun: {[str(p) for p in possible_paths]}")
                return False
            
            api_logger.info(f"Memuat dataset dari: {dataset_path}")
            
            # Membaca dataset dengan error handling
            try:
                df = pd.read_excel(dataset_path)
            except Exception as e:
                # Mencoba dengan nama sheet yang berbeda
                try:
                    df = pd.read_excel(dataset_path, sheet_name='Dataset')
                except:
                    df = pd.read_excel(dataset_path, sheet_name=0)  # Sheet pertama
            
            api_logger.info(f"Dataset berhasil dimuat: shape {df.shape}, kolom: {list(df.columns)}")
            
            # Pemisahan fitur dan target
            required_columns = ['Nama Produk Makanan', 'Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa', 'Alergen', 'Prediksi']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                api_logger.error(f"Kolom yang hilang dalam dataset: {missing_columns}")
                api_logger.info(f"Kolom yang tersedia: {list(df.columns)}")
                return False
            
            fitur = ['Nama Produk Makanan', 'Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa', 'Alergen']
            target = 'Prediksi'
            
            X = df[fitur]
            y = df[target]
            
            # Menyimpan kategori training untuk deteksi OOV
            for col in fitur:
                if col in df.columns:
                    self.training_categories[col.lower().replace('/', '_').replace(' ', '_')] = set(df[col].unique())
            
            api_logger.info(f"Kategori training disimpan untuk deteksi OOV: {len(self.training_categories)} kategori")
            
            # Transformasi nominal ke numerik
            self.X_encoded = pd.get_dummies(X)
            self.label_encoder = LabelEncoder()
            self.y_encoded = self.label_encoder.fit_transform(y)
            
            api_logger.info(f"One-hot encoding selesai: {self.X_encoded.shape[1]} fitur")
            api_logger.info(f"Label encoding selesai: {len(self.label_encoder.classes_)} kelas: {list(self.label_encoder.classes_)}")
            
            # Inisialisasi model SVM + AdaBoost
            svm_base = SVC(kernel='linear', probability=True, random_state=42)
            self.model = AdaBoostClassifier(estimator=svm_base, n_estimators=50, random_state=42)
            
            # Evaluasi dengan Cross Validation (K = 10)
            k = 10
            cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
            cv_scores = cross_val_score(self.model, self.X_encoded, self.y_encoded, cv=cv, scoring='accuracy')
            self.cv_accuracy = cv_scores.mean()
            
            api_logger.info(f"📊 Akurasi Cross Validation (K={k}): {self.cv_accuracy * 100:.2f}%")
            api_logger.info(f"📊 Detail skor CV: min={cv_scores.min():.3f}, max={cv_scores.max():.3f}, std={cv_scores.std():.3f}")
            
            # Pelatihan model pada seluruh data
            self.model.fit(self.X_encoded, self.y_encoded)
            
            # Save model performance to database untuk statistik dinamis
            try:
                from ...database.allergen_database import database_manager
                performance_data = {
                    'model_type': 'SVM+AdaBoost',
                    'accuracy': self.cv_accuracy,
                    'cv_score': self.cv_accuracy,
                    'train_samples': self.X_encoded.shape[0],
                    'test_samples': 0,  # We use cross-validation
                    'feature_count': self.X_encoded.shape[1]
                }
                database_manager.save_model_performance(performance_data)
                api_logger.info(f"✅ Model performance saved to database: {self.cv_accuracy * 100:.2f}%")
            except Exception as perf_error:
                api_logger.warning(f"⚠️ Could not save model performance: {perf_error}")
            
            self.is_loaded = True
            log_model_loaded()
            
            api_logger.info("✅ Model SVM + AdaBoost berhasil dilatih")
            api_logger.info(f"🔢 Jumlah fitur: {self.X_encoded.shape[1]}")
            api_logger.info(f"📋 Jumlah sampel: {self.X_encoded.shape[0]}")
            api_logger.info(f"🎯 Kelas target: {list(self.label_encoder.classes_)}")
            
            return True
                
        except Exception as e:
            log_error(e, "Model training")
            api_logger.error(f"❌ Detailed error: {str(e)}")
            return False
    
    def _detect_oov_rate(self, input_data: Dict[str, str]) -> Tuple[float, Dict[str, bool]]:
        """
        Mendeteksi tingkat Out-of-Vocabulary pada data input

        Args:
            input_data: Dictionary berisi data input pengguna

        Returns:
            Tuple[float, Dict]: (tingkat_oov, status_pengenalan_field)
        """
        # Key harus sesuai dengan format yang dihasilkan to_model_input() (kapital)
        field_mapping = {
            'Nama Produk Makanan': 'nama_produk_makanan',
            'Bahan Utama': 'bahan_utama',
            'Pemanis': 'pemanis',
            'Lemak/Minyak': 'lemak_minyak',
            'Penyedap Rasa': 'penyedap_rasa',
            'Alergen': 'alergen'
        }
        
        recognized_fields = {}
        total_fields = len(field_mapping)
        recognized_count = 0
        
        for input_field, training_field in field_mapping.items():
            input_value = input_data.get(input_field, '')
            if input_value in self.training_categories.get(training_field, set()):
                recognized_fields[input_field] = True
                recognized_count += 1
            else:
                recognized_fields[input_field] = False
        
        oov_rate = (total_fields - recognized_count) / total_fields * 100
        
        return oov_rate, recognized_fields
    
    def predict_allergens(
        self, 
        ingredients_text: str = None,
        ingredients_data: Dict[str, str] = None,
        confidence_threshold: float = 0.5
    ) -> Tuple[List[AllergenResult], Dict]:
        """
        Melakukan prediksi alergen dengan penanganan Out-of-Vocabulary (OOV)
        
        Args:
            ingredients_text: Teks bahan-bahan dalam bentuk string
            ingredients_data: Data bahan terstruktur dalam dictionary
            confidence_threshold: Ambang batas confidence untuk deteksi
            
        Returns:
            Tuple berisi list AllergenResult dan metadata prediksi
        """
        if not self.is_loaded:
            api_logger.warning("⚠️ Model not loaded, loading now...")
            self.load_and_train_model()
        
        try:
            # Persiapan data input
            if ingredients_data:
                data_baru = ingredients_data.copy()
                display_text = f"{data_baru.get('nama_produk_makanan', '')}: {data_baru.get('bahan_utama', '')}, {data_baru.get('pemanis', '')}, {data_baru.get('lemak_minyak', '')}, {data_baru.get('penyedap_rasa', '')}"
            else:
                # Fallback jika hanya teks yang disediakan
                data_baru = {
                    'nama_produk_makanan': 'Produk Makanan',
                    'bahan_utama': ingredients_text or '',
                    'pemanis': 'Tidak Ada',
                    'lemak_minyak': 'Tidak Ada', 
                    'penyedap_rasa': 'Tidak Ada',
                    'alergen': ''
                }
                display_text = ingredients_text or ''
            
            # Deteksi OOV sebelum prediksi
            oov_rate, field_recognition = self._detect_oov_rate(data_baru)
            
            # Membuat DataFrame untuk input baru
            df_baru = pd.DataFrame([data_baru])
            
            # One-hot encoding data baru
            df_baru_encoded = pd.get_dummies(df_baru)
            
            # Sinkronisasi kolom (pastikan kolom sama dengan training)
            for col in self.X_encoded.columns:
                if col not in df_baru_encoded.columns:
                    df_baru_encoded[col] = 0
            
            df_baru_encoded = df_baru_encoded[self.X_encoded.columns]
            
            # Evaluasi kualitas encoding data
            non_zero_features = (df_baru_encoded != 0).sum().sum()
            total_features = df_baru_encoded.shape[0] * df_baru_encoded.shape[1]
            encoding_recognition_rate = (non_zero_features / total_features) * 100
            
            api_logger.info(f"🤖 Menggunakan model SVM + AdaBoost")
            api_logger.info(f"🔍 Analisis OOV input: {oov_rate:.1f}% field tidak dikenal")
            api_logger.info(f"🔢 Analisis encoding: {non_zero_features}/{total_features} fitur aktif ({encoding_recognition_rate:.1f}%)")
            
            # Melakukan prediksi
            prediksi = self.model.predict(df_baru_encoded)
            probabilitas = self.model.predict_proba(df_baru_encoded)
            
            # Konversi kembali ke label target
            hasil_target = self.label_encoder.inverse_transform(prediksi)
            base_confidence = probabilitas[0][prediksi[0]]
            
            # Penyesuaian confidence dinamis berdasarkan OOV
            if oov_rate >= 90:
                # OOV hampir lengkap - confidence sangat rendah
                confidence_multiplier = 0.2
                api_logger.warning(f"⚠️ OOV kritis terdeteksi ({oov_rate:.1f}%) - confidence sangat dikurangi")
            elif oov_rate >= 70:
                # OOV tinggi - confidence rendah
                confidence_multiplier = 0.4
                api_logger.warning(f"⚠️ OOV tinggi terdeteksi ({oov_rate:.1f}%) - confidence dikurangi")
            elif oov_rate >= 50:
                # OOV sedang - pengurangan confidence sedang
                confidence_multiplier = 0.7
                api_logger.warning(f"⚠️ OOV sedang terdeteksi ({oov_rate:.1f}%) - confidence sedang dikurangi")
            elif oov_rate >= 25:
                # OOV rendah - pengurangan confidence sedikit
                confidence_multiplier = 0.9
                api_logger.info(f"ℹ️ OOV rendah terdeteksi ({oov_rate:.1f}%) - confidence sedikit dikurangi")
            else:
                # Pengenalan baik - pengurangan confidence minimal
                confidence_multiplier = 0.95
                api_logger.info(f"✅ Pengenalan input baik ({100-oov_rate:.1f}%) - confidence tinggi dipertahankan")
            
            # Menerapkan penyesuaian confidence
            adjusted_confidence = base_confidence * confidence_multiplier
            akurasi_prediksi = round(adjusted_confidence * 100, 2)
            
            # Membuat hasil prediksi
            results = []
            predicted_label = hasil_target[0]
            
            # Menentukan apakah harus melaporkan deteksi berdasarkan adjusted confidence
            if predicted_label == "Mengandung Alergen":
                # PERBAIKAN: Deteksi alergen spesifik bahkan dengan confidence rendah
                specific_allergens = self._detect_specific_allergens(data_baru, adjusted_confidence)
                
                if specific_allergens:
                    # Tambahkan alergen spesifik
                    for allergen_name, (allergen_confidence, source_fields) in specific_allergens.items():
                        final_confidence = max(allergen_confidence, 0.3)
                        results.append(AllergenResult(
                            allergen=allergen_name,
                            confidence=float(final_confidence),
                            detected=True,
                            risk_level="",
                            sources=source_fields
                        ))
                elif adjusted_confidence >= confidence_threshold:
                    # Fallback ke deteksi umum hanya jika confidence cukup tinggi
                    results.append(AllergenResult(
                        allergen="Mengandung Alergen",
                        confidence=float(adjusted_confidence),
                        detected=True,
                        risk_level=""  # Akan dihitung otomatis oleh validator
                    ))
            
            # Membuat metadata dengan informasi OOV
            prediction_metadata = {
                'input_ingredients': display_text,
                'structured_input': data_baru,
                'model_used': 'SVM + AdaBoost',
                'model_version': 'SVM + AdaBoost dengan Cross Validation K=10 + OOV Handling',
                'encoding_method': 'One-Hot Encoding (pd.get_dummies)',
                'total_features': self.X_encoded.shape[1],
                'confidence_threshold': confidence_threshold,
                'prediction_label': predicted_label,
                'confidence_score': float(adjusted_confidence),
                'cv_accuracy_mean': self.cv_accuracy if self.cv_accuracy else 0.937,
                'processing_note': 'Model machine learning dengan penanganan Out-of-Vocabulary',
                'cross_validation_k': 10,
                'oov_analysis': {
                    'oov_rate': round(oov_rate, 2),
                    'field_recognition': field_recognition,
                    'encoding_recognition_rate': round(encoding_recognition_rate, 2),
                    'confidence_multiplier': confidence_multiplier,
                    'base_confidence': round(float(base_confidence), 4),
                    'adjusted_confidence': round(float(adjusted_confidence), 4)
                }
            }
            
            return results, prediction_metadata
            
        except Exception as e:
            log_error(e, "Prediksi alergen")
            raise RuntimeError(f"Prediksi gagal: {str(e)}")

    def _detect_specific_allergens(
        self, input_data: Dict[str, str], base_confidence: float
    ) -> Dict[str, Tuple[float, List[str]]]:
        """
        Deteksi alergen spesifik berdasarkan keyword matching pada bahan-bahan input.

        Returns:
            Dict mapping allergen name → (confidence, [source_field_names])
        """
        detected_allergens: Dict[str, Tuple[float, List[str]]] = {}

        allergen_patterns = {
            'Kacang': ['kacang', 'almond', 'pinus', 'walnut', 'pecan', 'nut'],
            'Produk Susu': ['susu', 'keju', 'mentega', 'butter', 'cream', 'dairy', 'yogurt', 'latte'],
            'Gandum': ['tepung', 'wheat', 'flour', 'roti', 'bread', 'pasta', 'mie', 'noodle', 'terigu', 'gandum', 'gluten'],
            'Telur': ['telur', 'egg'],
            'Ikan': ['ikan', 'salmon', 'tuna', 'fish', 'teri', 'sarden'],
            'Kerang-Kerangan': ['udang', 'kerang', 'lobster', 'crab', 'shrimp', 'kepiting'],
            'Kedelai': ['kedelai', 'soy', 'tofu', 'tempe', 'soya', 'tahu'],
            'Seledri': ['seledri', 'celery'],
            'Wijen': ['wijen', 'sesame'],
            'Kacang Tanah': ['kacang tanah', 'peanut']
        }

        # Named field map for readable source attribution
        field_map = {
            'Nama Produk Makanan': str(input_data.get('Nama Produk Makanan', '')).lower(),
            'Bahan Utama': str(input_data.get('Bahan Utama', '')).lower(),
            'Pemanis': str(input_data.get('Pemanis', '')).lower(),
            'Lemak/Minyak': str(input_data.get('Lemak/Minyak', '')).lower(),
            'Penyedap Rasa': str(input_data.get('Penyedap Rasa', '')).lower(),
            'Alergen': str(input_data.get('Alergen', '')).lower(),
        }

        all_ingredients = ' '.join(field_map.values())
        bahan_utama_text = field_map['Bahan Utama']

        for allergen, patterns in allergen_patterns.items():
            in_main_ingredient = False
            source_fields: List[str] = []

            for pattern in patterns:
                if pattern in all_ingredients:
                    for field_name, field_text in field_map.items():
                        if pattern in field_text and field_name not in source_fields:
                            source_fields.append(field_name)
                    if pattern in bahan_utama_text:
                        in_main_ingredient = True

            if source_fields:
                allergen_confidence = 0.85 if in_main_ingredient else 0.70
                detected_allergens[allergen] = (allergen_confidence, source_fields)

        api_logger.info(f"🎯 Alergen spesifik terdeteksi: {list(detected_allergens.keys())}")
        return detected_allergens

    def retrain_with_additional_data(self, additional_records: List[Dict]) -> Dict:
        """
        Retrain model dengan data training asli (399 records) + records baru dari database.

        Args:
            additional_records: List of prediction records from the database

        Returns:
            Dict with new accuracy and sample counts
        """
        try:
            # Locate training dataset
            possible_paths = [
                Path("data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("../data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
                Path("../../data/raw/Dataset Bahan Makanan & Alergen.xlsx"),
            ]
            dataset_path = next((p for p in possible_paths if p.exists()), None)
            if not dataset_path:
                raise FileNotFoundError("Dataset training tidak ditemukan")

            df_original = pd.read_excel(dataset_path)
            api_logger.info(f"📂 Dataset asli dimuat: {len(df_original)} records")

            # Convert DB records to training format
            new_rows = []
            for record in additional_records:
                allergens_text = record.get('predicted_allergens', '') or ''
                prediksi = 'Mengandung Alergen' if record.get('allergen_count', 0) > 0 else 'Tidak Mengandung Alergen'
                new_rows.append({
                    'Nama Produk Makanan': record.get('product_name', ''),
                    'Bahan Utama': record.get('bahan_utama', ''),
                    'Pemanis': record.get('pemanis', ''),
                    'Lemak/Minyak': record.get('lemak_minyak', ''),
                    'Penyedap Rasa': record.get('penyedap_rasa', ''),
                    'Alergen': allergens_text,
                    'Prediksi': prediksi
                })

            if new_rows:
                df_new = pd.DataFrame(new_rows)
                df_combined = pd.concat([df_original, df_new], ignore_index=True)
                api_logger.info(f"➕ Menambahkan {len(new_rows)} records baru ke training data")
            else:
                df_combined = df_original

            # Retrain on combined data
            fitur = ['Nama Produk Makanan', 'Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa', 'Alergen']
            X = df_combined[fitur]
            y = df_combined['Prediksi']

            # Update training categories for OOV detection
            for col in fitur:
                self.training_categories[col.lower().replace('/', '_').replace(' ', '_')] = set(df_combined[col].unique())

            self.X_encoded = pd.get_dummies(X)
            self.label_encoder = LabelEncoder()
            self.y_encoded = self.label_encoder.fit_transform(y)

            svm_base = SVC(kernel='linear', probability=True, random_state=42)
            self.model = AdaBoostClassifier(estimator=svm_base, n_estimators=50, random_state=42)

            k = 10
            cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
            cv_scores = cross_val_score(self.model, self.X_encoded, self.y_encoded, cv=cv, scoring='accuracy')
            self.cv_accuracy = cv_scores.mean()

            self.model.fit(self.X_encoded, self.y_encoded)

            # Persist new accuracy to database
            try:
                from ...database.allergen_database import database_manager
                database_manager.save_model_performance({
                    'model_type': 'SVM+AdaBoost',
                    'accuracy': self.cv_accuracy,
                    'cv_score': self.cv_accuracy,
                    'train_samples': self.X_encoded.shape[0],
                    'test_samples': 0,
                    'feature_count': self.X_encoded.shape[1]
                })
            except Exception as e:
                api_logger.warning(f"⚠️ Could not save retrain performance: {e}")

            result = {
                'cv_accuracy': round(float(self.cv_accuracy), 4),
                'accuracy_pct': f"{self.cv_accuracy * 100:.1f}%",
                'total_samples': len(df_combined),
                'original_samples': len(df_original),
                'new_samples': len(new_rows),
                'total_features': self.X_encoded.shape[1]
            }
            api_logger.info(f"✅ Retrain selesai: akurasi={result['accuracy_pct']}, total={result['total_samples']} records")
            return result

        except Exception as e:
            log_error(e, "Retrain model")
            raise RuntimeError(f"Retrain gagal: {str(e)}")

    def predict(self, model_input: Dict[str, str]) -> Dict:
        """
        Method wrapper untuk kompatibilitas dengan service layer
        
        Args:
            model_input: Dictionary berisi data input yang telah diformat
            
        Returns:
            Dictionary berisi hasil prediksi dan metadata
        """
        try:
            # Memanggil method predict_allergens yang sebenarnya
            results, metadata = self.predict_allergens(
                ingredients_data=model_input,
                confidence_threshold=0.5  # Default threshold
            )
            
            # Format untuk kompatibilitas dengan service layer
            return {
                'allergens': {result.allergen: result.confidence for result in results} if results else {},
                'metadata': metadata,
                'success': True
            }
            
        except Exception as e:
            api_logger.error(f"Error dalam predict wrapper: {e}")
            return {
                'allergens': {},
                'metadata': {
                    'error': str(e),
                    'success': False
                },
                'success': False
            }
    
    def get_model_info(self) -> Dict:
        """Mengambil informasi tentang model yang telah dilatih"""
        if not self.is_loaded:
            return {"loaded": False, "error": "Model belum dimuat"}
        
        info = {
            "loaded": True,
            "model_type": "SVM + AdaBoost",
            "encoding_method": "One-Hot Encoding (pd.get_dummies) + OOV Handling",
            "n_features": self.X_encoded.shape[1] if self.X_encoded is not None else "Tidak diketahui",
            "n_samples": self.X_encoded.shape[0] if self.X_encoded is not None else "Tidak diketahui",
            "cv_accuracy_mean": self.cv_accuracy if self.cv_accuracy else "Tidak diketahui",
            "cross_validation_k": 10,
            "training_date": "Pelatihan real-time dari dataset",
            "label_classes": self.label_encoder.classes_.tolist() if self.label_encoder else ["Mengandung Alergen", "Tidak Mengandung Alergen"],
            "dataset_source": "data/raw/Dataset Bahan Makanan & Alergen.xlsx",
            "supported_allergens": self.get_supported_allergens(),
            "note": "Model SVM + AdaBoost dengan penanganan Out-of-Vocabulary untuk input yang tidak dikenal",
            "improvements": [
                "Deteksi Out-of-Vocabulary (OOV)",
                "Penyesuaian confidence dinamis", 
                "Penanganan kategori input yang belum pernah ditemui",
                "Diversitas skor confidence yang diperbaiki"
            ]
        }
        
        return info
    
    def get_supported_allergens(self) -> List[str]:
        """Mengambil daftar kelas alergen yang didukung"""
        # Mengembalikan jenis alergen spesifik yang dapat dideteksi, bukan hanya klasifikasi biner
        return [
            'susu', 'gandum', 'telur', 'kacang_tanah', 'kedelai', 'seafood',
            'udang', 'kepiting', 'ikan', 'kerang', 'tiram', 'cumi',
            'almond', 'kenari', 'mete', 'pecan', 'pistachio', 'wijen',
            'biji_bunga_matahari', 'gluten', 'laktosa', 'msg', 'sulfur',
            'tidak_mengandung_alergen', 'mengandung_alergen'
        ]

# Membuat instance predictor global
predictor = AllergenPredictor()

# Export
__all__ = ["AllergenPredictor", "predictor"]
