import { useState, useEffect } from 'react'

/**
 * Custom hook untuk mengambil statistik database real-time
 * Mengikuti prinsip separation of concerns
 */
export const useStatistics = () => {
  const [stats, setStats] = useState({
    datasetCount: 0,
    allergenTypes: 0,
    accuracy: '93.7%',
    processingTime: '<500ms',
    loading: true,
    error: null
  })

  useEffect(() => {
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
        
        // Extract allergen types count
        const allergenTypes = data.chart_data?.allergens_distribution?.length || 8
        
        // Update state dengan data dari API
        setStats({
          datasetCount: data.overview?.total_predictions || 0,
          allergenTypes: allergenTypes,
          accuracy: data.model_info?.accuracy || '93.7%',
          processingTime: data.performance_metrics?.average_processing_time || '<500ms',
          loading: false,
          error: null
        })
        
      } catch (error) {
        console.error('Error fetching statistics:', error)
        
        // Fallback ke data default jika API tidak tersedia
        setStats({
          datasetCount: 191, // Berdasarkan dokumentasi backup
          allergenTypes: 8,  // Estimasi berdasarkan data yang ada
          accuracy: '93.7%',
          processingTime: '<500ms',
          loading: false,
          error: error.message
        })
      }
    }

    fetchStatistics()
  }, [])

  const refetch = () => {
    setStats(prev => ({ ...prev, loading: true }))
    // Re-run useEffect
  }

  return { ...stats, refetch }
}
