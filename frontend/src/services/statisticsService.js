/**
 * Service untuk mengelola statistik aplikasi
 * Menyediakan fungsi untuk update statistik otomatis
 */

class StatisticsService {
  constructor() {
    this.listeners = []
    this.lastStats = null
  }

  /**
   * Subscribe untuk perubahan statistik
   */
  subscribe(callback) {
    this.listeners.push(callback)
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback)
    }
  }

  /**
   * Notify semua listeners tentang perubahan statistik
   */
  notifyListeners(stats) {
    this.lastStats = stats
    this.listeners.forEach(callback => callback(stats))
  }

  /**
   * Update dataset count setelah deteksi alergen
   */
  async incrementDatasetCount() {
    try {
      // Fetch statistik terbaru
      const response = await fetch('/api/v1/dataset/statistics')
      if (!response.ok) return

      const result = await response.json()
      const updatedStats = {
        datasetCount: result.data.overview?.total_predictions || 0,
        accuracy: result.data.model_info?.accuracy || '93.7%',
        processingTime: result.data.performance_metrics?.average_processing_time || '<500ms'
      }

      this.notifyListeners(updatedStats)
      return updatedStats
    } catch (error) {
      console.error('Error updating statistics:', error)
    }
  }

  /**
   * Update accuracy berdasarkan performance model terbaru
   */
  async updateModelAccuracy(newAccuracy) {
    if (this.lastStats) {
      const updatedStats = {
        ...this.lastStats,
        accuracy: `${newAccuracy.toFixed(1)}%`
      }
      this.notifyListeners(updatedStats)
    }
  }

  /**
   * Update processing time berdasarkan deteksi terbaru
   */
  async updateProcessingTime(processingTimeMs) {
    if (this.lastStats) {
      const timeDisplay = processingTimeMs < 1000 
        ? `<${Math.ceil(processingTimeMs)}ms`
        : `${(processingTimeMs/1000).toFixed(1)}s`
      
      const updatedStats = {
        ...this.lastStats,
        processingTime: timeDisplay
      }
      this.notifyListeners(updatedStats)
    }
  }

  /**
   * Get cached statistics
   */
  getCachedStats() {
    return this.lastStats
  }
}

// Export singleton instance
export const statisticsService = new StatisticsService()
export default statisticsService
