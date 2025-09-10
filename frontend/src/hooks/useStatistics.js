import { useState, useEffect } from 'react'
import { statisticsService } from '../services/statisticsService'

/**
 * Custom hook untuk mengambil statistik database real-time
 * Mengikuti prinsip separation of concerns dan auto-update
 */
export const useStatistics = () => {
  const [stats, setStats] = useState({
    datasetCount: 0,
    accuracy: '93.7%',
    processingTime: '<500ms',
    loading: true,
    error: null
  })

  const fetchStatistics = async () => {
    try {
      setStats(prev => ({ ...prev, loading: true, error: null }))
      
      // Ambil statistik dari API
      const response = await fetch('/api/v1/dataset/statistics')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      const data = result.data // API response format: { success: true, data: {...} }
      
      // Update state dengan data dinamis dari API
      const newStats = {
        datasetCount: data.overview?.total_predictions || 0,
        accuracy: data.model_info?.accuracy || '93.7%',
        processingTime: data.performance_metrics?.average_processing_time || '<500ms',
        loading: false,
        error: null
      }
      
      setStats(newStats)
      
      // Notify service untuk cache
      statisticsService.notifyListeners(newStats)
      
    } catch (error) {
      console.error('Error fetching statistics:', error)
      
      // Fallback ke data default jika API tidak tersedia
      setStats({
        datasetCount: 191, // Berdasarkan dokumentasi backup
        accuracy: '93.7%',
        processingTime: '<500ms',
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
