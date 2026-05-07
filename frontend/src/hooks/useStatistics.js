import { useState, useEffect } from 'react'
import { statisticsService } from '../services/statisticsService'

/**
 * Custom hook untuk mengambil statistik database real-time
 * Mengikuti prinsip separation of concerns dan auto-update
 */
export const useStatistics = () => {
  const cached = statisticsService.getCachedStats()
  const [stats, setStats] = useState({
    datasetCount: cached?.datasetCount || 0,
    accuracy: cached?.accuracy || '93.7%',
    processingTime: cached?.processingTime || '<500ms',
    loading: true,
    error: null
  })

  const fetchStatistics = async () => {
    try {
      setStats(prev => ({ ...prev, loading: true, error: null }))

      const response = await fetch('/api/v1/dataset/statistics')

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      const data = result.data

      // Gunakan lastDetectionTime dari service jika tersedia (waktu deteksi terakhir)
      const displayProcessingTime = statisticsService.lastDetectionTime
        || data.performance_metrics?.average_processing_time
        || '<500ms'

      const newStats = {
        datasetCount: data.overview?.total_predictions || 0,
        accuracy: data.model_info?.accuracy || '93.7%',
        processingTime: displayProcessingTime,
        loading: false,
        error: null
      }

      setStats(newStats)
      statisticsService.notifyListeners(newStats)

    } catch (error) {
      console.error('Error fetching statistics:', error)

      setStats({
        datasetCount: statisticsService.getCachedStats()?.datasetCount || 191,
        accuracy: statisticsService.getCachedStats()?.accuracy || '93.7%',
        processingTime: statisticsService.lastDetectionTime || '<500ms',
        loading: false,
        error: error.message
      })
    }
  }

  useEffect(() => {
    fetchStatistics()

    // Subscribe untuk auto-update dari service
    const unsubscribe = statisticsService.subscribe((updatedStats) => {
      setStats(prev => ({
        ...prev,
        ...updatedStats,
        loading: false,
        error: null
      }))
    })

    return unsubscribe
  }, [])

  const refetch = () => {
    fetchStatistics()
  }

  return { ...stats, refetch }
}
