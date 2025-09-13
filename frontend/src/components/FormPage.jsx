import { useState } from 'react'
import { Send, AlertCircle, CheckCircle, ArrowLeft, Sparkles, Target } from 'lucide-react'
import Card from './UI/Card'
import Button from './UI/Button'
import { LoadingSpinner } from './UI/Loading'
import { predictAllergen } from '../services/api'
import { statisticsService } from '../services/statisticsService'

// Helper function to calculate confidence from API response
const calculateConfidence = (result) => {
  if (!result) return 0.0
  
  // 🔧 FIX: Always use backend's calculated confidence score first
  // This ensures consistency between frontend display and database
  if (result.confidence_score) return result.confidence_score * 100
  if (result.overall_confidence) return result.overall_confidence * 100
  
  // Fallback: Use detected allergens confidence if available
  if (result.detected_allergens && result.detected_allergens.length > 0) {
    const totalConfidence = result.detected_allergens.reduce((sum, allergen) => sum + (allergen.confidence || 0), 0)
    return (totalConfidence / result.detected_allergens.length) * 100
  }
  
  // Last resort default (should rarely be used)
  return 50.0
}

// Helper function to format confidence display
const formatConfidence = (result) => {
  const confidence = calculateConfidence(result)
  return confidence.toFixed(1) + '%'
}

function FormPage({ onNavigate, onDetectionResult }) {
  const [formData, setFormData] = useState({
    nama_produk_makanan: '',
    bahan_utama: '',
    pemanis: '',
    lemak_minyak: '', 
    penyedap_rasa: '',
    alergen: ''
  })
  
  // Opsi dropdown untuk alergen - sesuai dengan algoritma machine learning
  const allergenOptions = [
    { value: '', label: 'Pilih alergen yang akan dideteksi (wajib)' },
    { value: 'Tidak Ada', label: 'Tidak Ada Alergen' },
    { value: 'gandum', label: 'Gandum/Gluten' },
    { value: 'susu', label: 'Susu/Dairy' },
    { value: 'telur', label: 'Telur' },
    { value: 'kacang tanah', label: 'Kacang Tanah' },
    { value: 'kedelai', label: 'Kedelai/Soy' },
    { value: 'ikan', label: 'Ikan' },
    { value: 'udang', label: 'Udang/Shellfish' },
    { value: 'kepiting', label: 'Kepiting' },
    { value: 'wijen', label: 'Wijen' },
    { value: 'almond', label: 'Almond/Tree Nuts' }
  ]
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    // Validasi form - alergen wajib dipilih
    if (!formData.alergen || formData.alergen === '') {
      setError('Silakan pilih jenis alergen yang akan dideteksi')
      setLoading(false)
      return
    }
    
    try {
      const startTime = Date.now()
      const response = await predictAllergen(formData)
      const processingTime = Date.now() - startTime
      
      setResult(response)
      
      // Update statistik secara real-time
      await statisticsService.incrementDatasetCount()
      
      // Update processing time jika ada data
      if (processingTime) {
        await statisticsService.updateProcessingTime(processingTime)
      }
      
      // Update model accuracy jika ada confidence score
      if (response?.confidence_score || response?.overall_confidence) {
        const accuracy = (response.confidence_score || response.overall_confidence) * 100
        await statisticsService.updateModelAccuracy(accuracy)
      }
      
      if (onDetectionResult) {
        onDetectionResult(response)
      }
    } catch (err) {
      setError(err.message || 'Terjadi kesalahan saat prediksi')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Back Button */}
        <div className="mb-8">
          <Button
            variant="secondary"
            onClick={() => onNavigate && onNavigate('dashboard')}
            className="bg-white hover:bg-slate-50 border-2 border-slate-200 hover:border-slate-300 shadow-sm rounded-2xl"
          >
            <ArrowLeft className="h-5 w-5 mr-3" />
            Kembali ke Home
          </Button>
        </div>

        {/* Modern Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-4 bg-gradient-to-r from-blue-600 to-blue-700 rounded-3xl shadow-xl mb-6">
            <Target className="h-8 w-8 text-white mr-3" />
            <h1 className="text-3xl font-bold text-white">Deteksi Alergen Makanan</h1>
          </div>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Masukan kandungan produk pangan untuk mendeteksi alergen menggunakan  
            <span className="font-semibold text-blue-600"> algoritma SVM + AdaBoost</span>
          </p>
        </div>

        <div className="grid lg:grid-cols-5 gap-12">
          {/* Form Section - Takes 3 columns */}
          <div className="lg:col-span-3">
            <Card className="bg-white shadow-2xl border-0 rounded-3xl overflow-hidden">
              {/* Form Header */}
              <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6">
                <h2 className="text-2xl font-bold text-white mb-2">Form Analisis Produk</h2>
                <p className="text-slate-300">Lengkapi data produk makanan untuk deteksi alergen</p>
              </div>

              <div className="p-8">
                <form onSubmit={handleSubmit} className="space-y-8">
                  
                  {/* Nama Produk - Full Width */}
                  <div className="space-y-3">
                    <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                      Nama Produk Makanan *
                    </label>
                    <input
                      type="text"
                      name="nama_produk_makanan"
                      value={formData.nama_produk_makanan}
                      onChange={handleChange}
                      required
                      placeholder="Contoh: Roti Tawar, Keju Mozzarella, Biskuit Coklat"
                      className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                    />
                  </div>

                  {/* Bahan Utama - Full Width */}
                  <div className="space-y-3">
                    <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                      Bahan Utama *
                    </label>
                    <textarea
                      name="bahan_utama"
                      value={formData.bahan_utama}
                      onChange={handleChange}
                      required
                      rows={4}
                      placeholder="Contoh: Tepung terigu, telur, susu segar, mentega, gula pasir, garam"
                      className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white resize-none"
                    />
                    <p className="text-sm text-slate-500">
                      Tuliskan semua bahan utama yang digunakan, pisahkan dengan koma
                    </p>
                  </div>

                  {/* Grid dengan 2 kolom untuk field tambahan */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                      <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                        Pemanis
                      </label>
                      <input
                        type="text"
                        name="pemanis"
                        value={formData.pemanis}
                        onChange={handleChange}
                        placeholder="Contoh: Gula pasir, madu, sirup jagung"
                        className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      />
                    </div>

                    <div className="space-y-3">
                      <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                        Lemak/Minyak
                      </label>
                      <input
                        type="text"
                        name="lemak_minyak"
                        value={formData.lemak_minyak}
                        onChange={handleChange}
                        placeholder="Contoh: Mentega, minyak kelapa sawit"
                        className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      />
                    </div>
                  </div>

                  {/* Penyedap Rasa - Full Width */}
                  <div className="space-y-3">
                    <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                      Penyedap Rasa
                    </label>
                    <input
                      type="text"
                      name="penyedap_rasa"
                      value={formData.penyedap_rasa}
                      onChange={handleChange}
                      placeholder="Contoh: Garam, MSG, vanilla, kayu manis"
                      className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                    />
                  </div>

                  {/* Dropdown Alergen - Full Width */}
                  <div className="space-y-3">
                    <label className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                      Alergen yang Diketahui (Wajib Dipilih) <span className="text-red-500">*</span>
                    </label>
                    <div className="relative">
                      <select
                        name="alergen"
                        value={formData.alergen}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white appearance-none cursor-pointer"
                      >
                        {allergenOptions.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                      <div className="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                        <svg className="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>
                    <p className="text-sm text-slate-500">
                      Wajib pilih jenis alergen yang mungkin terkandung dalam produk ini untuk deteksi yang akurat
                    </p>
                  </div>

                  {/* Submit Button */}
                  <div className="flex justify-center pt-6">
                    <Button
                      type="submit"
                      size="lg"
                      disabled={loading}
                      className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-12 py-4 text-lg font-bold rounded-2xl shadow-2xl hover:shadow-blue-500/25 transform hover:scale-105 transition-all duration-300"
                    >
                      {loading ? (
                        <>
                          <LoadingSpinner size="md" className="mr-3" />
                          Menganalisis...
                        </>
                      ) : (
                        <>
                          <Send className="h-6 w-6 mr-3" />
                          Deteksi Alergen
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </div>
            </Card>
          </div>

          {/* Result Section - Takes 2 columns */}
          <div className="lg:col-span-2">
            <div className="sticky top-8">
              {/* Error Display */}
              {error && (
                <Card className="bg-gradient-to-r from-red-50 to-red-100 border-red-200 p-6 mb-6 rounded-2xl">
                  <div className="flex items-center">
                    <div className="p-2 bg-red-600 rounded-full mr-4">
                      <AlertCircle className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-red-800 mb-1">Error</h3>
                      <p className="text-red-700">{error}</p>
                    </div>
                  </div>
                </Card>
              )}

              {/* Result Display */}
              {result && (
                <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200 p-8 rounded-3xl shadow-xl">
                  <div className="text-center mb-6">
                    <div className="p-4 bg-green-600 rounded-full w-fit mx-auto mb-4">
                      <CheckCircle className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-green-900 mb-2">Hasil Deteksi</h3>
                    <p className="text-green-700">Produk: <span className="font-semibold">{result.product_name}</span></p>
                  </div>

                  <div className="space-y-6">
                    {/* Prediction Result */}
                    <div className="bg-white rounded-2xl p-6 shadow-sm">
                      <h4 className="font-bold text-slate-900 mb-3 flex items-center">
                        <Target className="h-5 w-5 mr-2 text-blue-600" />
                        Status Alergen
                      </h4>
                      <div className={`p-6 rounded-xl border-2 ${
                        result.total_allergens_detected === 0 
                          ? 'bg-green-50 text-green-900 border-green-300'
                          : 'bg-red-50 text-red-900 border-red-300'
                      }`}>
                        <div className="flex items-center justify-center mb-3">
                          {result.total_allergens_detected === 0 ? (
                            <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
                          ) : (
                            <AlertCircle className="h-8 w-8 text-red-600 mr-3" />
                          )}
                          <p className="font-bold text-xl">
                            {result.total_allergens_detected === 0 
                              ? 'AMAN - Tidak Mengandung Alergen' 
                              : `PERHATIAN - Mengandung ${result.total_allergens_detected} Alergen`}
                          </p>
                        </div>
                        {result.total_allergens_detected > 0 && result.detected_allergens && (
                          <div className="text-center">
                            <p className="text-sm font-semibold mb-2">Alergen yang Terdeteksi:</p>
                            <div className="flex flex-wrap justify-center gap-2">
                              {result.detected_allergens.map((a, idx) => (
                                <span key={idx} className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                                  {a.allergen}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Accuracy */}
                    <div className="bg-white rounded-2xl p-6 shadow-sm">
                      <h4 className="font-bold text-slate-900 mb-3">Accuracy</h4>
                      <div className="flex items-center space-x-4">
                        <div className="flex-1 bg-slate-200 rounded-full h-3">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-1000"
                            style={{ width: `${calculateConfidence(result)}%` }}
                          />
                        </div>
                        <span className="text-2xl font-bold text-blue-600">
                          {formatConfidence(result)}
                        </span>
                      </div>
                    </div>

                    {/* Additional Info */}
                    <div className="bg-white rounded-2xl p-6 shadow-sm">
                      <h4 className="font-bold text-slate-900 mb-3">Detail Deteksi</h4>
                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-600">Algoritma:</span>
                          <span className="font-semibold">SVM + AdaBoost</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-600">Processing Time:</span>
                          <span className="font-semibold">{result.processing_time?.toFixed(0) || 'N/A'}ms</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-600">Model Version:</span>
                          <span className="font-semibold text-xs">K-10 CV + OOV</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              )}

              {/* Info Panel - Show when no result */}
              {!result && !loading && (
                <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 p-8 rounded-3xl">
                  <div className="text-center">
                    <div className="p-4 bg-blue-600 rounded-full w-fit mx-auto mb-4">
                      <Sparkles className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-blue-900 mb-3">Siap untuk Analisis</h3>
                    <p className="text-blue-700 mb-6">
                      Lengkapi form di sebelah kiri untuk memulai deteksi alergen dengan teknologi AI
                    </p>
                    
                    {/* Features */}
                    <div className="space-y-3 text-left">
                      <div className="flex items-center text-blue-800">
                        <CheckCircle className="h-5 w-5 mr-3 text-blue-600" />
                        <span className="font-medium">Akurasi model dinamis</span>
                      </div>
                      <div className="flex items-center text-blue-800">
                        <CheckCircle className="h-5 w-5 mr-3 text-blue-600" />
                        <span className="font-medium">Deteksi komprehensif alergen</span>
                      </div>
                      <div className="flex items-center text-blue-800">
                        <CheckCircle className="h-5 w-5 mr-3 text-blue-600" />
                        <span className="font-medium">Hasil instan dalam detik</span>
                      </div>
                    </div>
                  </div>
                </Card>
              )}
            </div>
          </div>
        </div>

        {/* Institutional Footer */}
        <div className="mt-16 pt-8 border-t border-slate-200">
          <div className="text-center">
            <p className="text-slate-500 text-sm">
              Powered by <span className="font-semibold">Universitas Nasional Karangturi</span> • 
              Supported by <span className="font-semibold">Direktorat Penelitian dan Pengabdian kepada Masyarakat (DPPM) - Kementrian Pendidikan Tinggi, Sains dan Teknologi, Direktorat Jendral Riset dan Pengembangan</span>
            </p>
            <p className="text-slate-400 text-xs mt-2">
              © 2025 SuperBoost-AllerScan Aplikasi Deteksi Alergen Berbasis Data Mining & Machine Learning
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FormPage
