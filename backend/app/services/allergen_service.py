"""
Layer Service untuk Deteksi Alergen

Implementasi service layer untuk memisahkan business logic dari API routes.
Menerapkan prinsip arsitektur bersih dengan pemisahan tanggung jawab yang jelas.

Fitur utama:
- Validasi data input pengguna
- Integrasi dengan machine learning model
- Pemrosesan dan formatting hasil prediksi  
- Penyimpanan data ke database
- Error handling yang komprehensif
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import traceback

from ...core.logger import api_logger
from ...database.allergen_database import database_manager
from ...models.inference.predictor import predictor
from ...schemas.request_schemas import PredictionRequest, PredictionResponse, AllergenResult

class AllergenDetectionService:
    """
    Service class untuk deteksi alergen dalam produk makanan
    
    Tanggung jawab utama:
    - Memvalidasi data input pengguna
    - Memanggil model machine learning untuk prediksi
    - Memproses dan memformat hasil prediksi
    - Menyimpan hasil ke database
    - Menangani error dengan graceful handling
    """
    
    def __init__(self):
        self.predictor = predictor
        self.db = database_manager
    
    async def detect_allergens(self, request: PredictionRequest, client_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Method utama untuk deteksi alergen dalam produk makanan
        
        Args:
            request: Object PredictionRequest berisi data input
            client_info: Informasi client opsional (IP, user agent, dll)
            
        Returns:
            Dictionary berisi hasil prediksi dan metadata
        """
        start_time = time.time()
        
        try:
            # Validasi ketersediaan model
            if not self.predictor.is_loaded:
                raise ValueError("Model sedang dimuat. Silakan coba lagi dalam beberapa saat.")
            
            # Persiapan input untuk model
            model_input = request.to_model_input()
            api_logger.info(f"Memproses permintaan prediksi untuk: {request.nama_produk_makanan}")
            
            # Panggil model machine learning
            prediction_result = self.predictor.predict(model_input)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Proses hasil prediksi
            formatted_result = self._format_prediction_result(
                prediction_result, 
                request, 
                processing_time
            )
            
            # Simpan ke database
            await self._save_prediction_to_database(
                formatted_result, 
                request, 
                client_info
            )
            
            api_logger.info(f"Prediksi selesai dalam {processing_time:.2f}ms")
            return formatted_result
            
        except Exception as e:
            error_msg = f"Terjadi kesalahan dalam deteksi alergen: {str(e)}"
            api_logger.error(f"Error: {error_msg}")
            api_logger.error(f"Traceback: {traceback.format_exc()}")
            
            return {
                'success': False,
                'error': True,
                'message': error_msg,
                'error_code': 'PREDICTION_ERROR',
                'timestamp': datetime.now(),
                'processing_time_ms': (time.time() - start_time) * 1000
            }
    
    def _format_prediction_result(self, raw_result: Dict, request: PredictionRequest, processing_time: float) -> Dict:
        """
        Memformat hasil prediksi machine learning menjadi response yang terstruktur
        
        Args:
            raw_result: Hasil mentah dari model machine learning
            request: Permintaan asli dari pengguna
            processing_time: Waktu pemrosesan dalam milliseconds
            
        Returns:
            Hasil prediksi yang sudah diformat dengan metadata lengkap
        """
        try:
            # Ekstrak alergen dari hasil mentah model
            detected_allergens = []
            
            # Parsing hasil prediksi sesuai format output model
            if 'allergens' in raw_result:
                allergen_data = raw_result['allergens']
                
                for allergen_name, confidence in allergen_data.items():
                    if confidence >= request.confidence_threshold:
                        detected_allergens.append(
                            AllergenResult(
                                allergen=allergen_name,
                                confidence=float(confidence),
                                risk_level=self._determine_risk_level(confidence),
                                detected=True
                            )
                        )
            
            # Hitung metrik keseluruhan
            total_detected = len(detected_allergens)
            overall_confidence = sum(a.confidence for a in detected_allergens) / max(total_detected, 1)
            overall_risk = self._determine_overall_risk(detected_allergens)
            
            # Buat string ingredients
            ingredients_list = [
                request.bahan_utama,
                request.pemanis if request.pemanis != "Tidak Ada" else "",
                request.lemak_minyak if request.lemak_minyak != "Tidak Ada" else "",
                request.penyedap_rasa if request.penyedap_rasa != "Tidak Ada" else ""
            ]
            processed_text = ", ".join(filter(None, ingredients_list))
            
            return {
                'success': True,
                'detected_allergens': [a.dict() for a in detected_allergens],
                'total_allergens_detected': total_detected,
                'processing_time_ms': processing_time,
                'model_version': raw_result.get('model_version', 'SVM+AdaBoost v1.0'),
                'confidence_threshold': request.confidence_threshold,
                'processed_text': processed_text,
                'input_length': len(processed_text),
                'overall_risk': overall_risk,
                'timestamp': datetime.now(),
                
                # Metadata tambahan
                'product_name': request.nama_produk_makanan,
                'ingredients': processed_text,
                'allergen_summary': ', '.join([a.allergen for a in detected_allergens]) if detected_allergens else 'tidak terdeteksi'
            }
            
        except Exception as e:
            api_logger.error(f"Error dalam memformat hasil prediksi: {e}")
            raise
    
    def _determine_risk_level(self, confidence: float) -> str:
        """Menentukan tingkat risiko berdasarkan skor confidence"""
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _determine_overall_risk(self, detected_allergens: List[AllergenResult]) -> str:
        """Menentukan tingkat risiko keseluruhan berdasarkan alergen yang terdeteksi"""
        if not detected_allergens:
            return "none"
        
        max_confidence = max(a.confidence for a in detected_allergens)
        allergen_count = len(detected_allergens)
        
        if max_confidence >= 0.8 or allergen_count > 2:
            return "high"
        elif max_confidence >= 0.5 or allergen_count > 1:
            return "medium"
        else:
            return "low"
    
    async def _save_prediction_to_database(self, result: Dict, request: PredictionRequest, client_info: Optional[Dict]):
        """Menyimpan hasil prediksi ke database untuk riwayat dan analisis"""
        try:
            prediction_data = {
                'productName': request.nama_produk_makanan,
                'bahan_utama': request.bahan_utama,
                'pemanis': request.pemanis if request.pemanis else 'Tidak Ada',
                'lemak_minyak': request.lemak_minyak if request.lemak_minyak else 'Tidak Ada',
                'penyedap_rasa': request.penyedap_rasa if request.penyedap_rasa else 'Tidak Ada',
                'ingredients': result['processed_text'],
                'allergens': result['allergen_summary'],
                'allergen_count': result['total_allergens_detected'],
                'confidence': result.get('detected_allergens', [{}])[0].get('confidence', 0.0) if result.get('detected_allergens') else 0.95,
                'risk_level': result['overall_risk'],
                'processing_time_ms': result['processing_time_ms'],
                'model_version': result['model_version'],
                'user_ip': client_info.get('client_ip', '') if client_info else '',
                'user_agent': client_info.get('user_agent', '') if client_info else ''
            }
            
            record_id = self.db.save_prediction_result(prediction_data)
            result['database_id'] = record_id
            
        except Exception as e:
            api_logger.error(f"Error dalam penyimpanan ke database: {e}")
            # Tidak menggagalkan seluruh request jika penyimpanan database gagal
    
    async def get_supported_allergens(self) -> List[str]:
        """Mengambil daftar alergen yang didukung oleh model"""
        try:
            if not self.predictor.is_loaded:
                # Return daftar fallback standar
                return [
                    'susu', 'gandum', 'telur', 'kacang_tanah', 'kedelai', 'seafood',
                    'udang', 'kepiting', 'ikan', 'kerang', 'tiram', 'cumi',
                    'almond', 'kenari', 'mete', 'pecan', 'pistachio', 'wijen',
                    'biji_bunga_matahari', 'gluten', 'laktosa', 'msg', 'sulfur'
                ]
            
            # Ambil dari model jika tersedia
            return self.predictor.get_supported_allergens()
            
        except Exception as e:
            api_logger.error(f"Error dalam mengambil daftar alergen: {e}")
            return []
    
    async def get_model_info(self) -> Dict:
        """Mengambil informasi detail tentang model machine learning yang digunakan"""
        try:
            return {
                'model_type': 'SVM + AdaBoost',
                'version': '1.0.0',
                'is_loaded': self.predictor.is_loaded,
                'supported_allergens_count': len(await self.get_supported_allergens()),
                'accuracy': '93.7%',
                'cross_validation': 'K-Fold (k=10)',
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            api_logger.error(f"Error dalam mengambil informasi model: {e}")
            return {'error': str(e)}

# Buat instance singleton
allergen_service = AllergenDetectionService()

# Export untuk penggunaan di modul lain
__all__ = ['AllergenDetectionService', 'allergen_service']
