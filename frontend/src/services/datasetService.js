import api from './api'

// Dataset API functions
export const getDataset = async (page = 1, pageSize = 10) => {
  try {
    const response = await api.get('/api/v1/dataset/predictions', {
      params: { page, page_size: pageSize }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching dataset:', error)
    throw new Error('Failed to fetch dataset')
  }
}

// Get all predictions (fetch all pages)
export const getAllPredictions = async () => {
  try {
    // First, get the first page to see total pages
    const firstResponse = await api.get('/api/v1/dataset/predictions', {
      params: { page: 1, page_size: 10 }
    })
    
    const firstData = firstResponse.data
    const totalPages = firstData.data?.pagination?.total_pages || 1
    const allPredictions = firstData.data?.predictions || []
    
    // If there are more pages, fetch them
    if (totalPages > 1) {
      const promises = []
      for (let page = 2; page <= totalPages; page++) {
        promises.push(
          api.get('/api/v1/dataset/predictions', {
            params: { page, page_size: 10 }
          })
        )
      }
      
      const responses = await Promise.all(promises)
      responses.forEach(response => {
        if (response.data?.data?.predictions) {
          allPredictions.push(...response.data.data.predictions)
        }
      })
    }
    
    return {
      ...firstData,
      data: {
        ...firstData.data,
        predictions: allPredictions
      }
    }
  } catch (error) {
    console.error('Error fetching all predictions:', error)
    throw new Error('Failed to fetch all predictions')
  }
}

export const getPredictionHistory = async (options = {}) => {
  try {
    const { page = 1, limit = 100, includeStats = false } = options
    const response = await api.get('/api/v1/dataset/predictions', {
      params: { page, page_size: limit }
    })
    
    // Backend response format
    const data = response.data?.data || response.data
    
    return {
      predictions: data.predictions || [],
      statistics: data.statistics || null,
      pagination: data.pagination || { total_items: 0, total_pages: 0 }
    }
  } catch (error) {
    console.error('Error fetching prediction history:', error)
    throw new Error('Failed to fetch prediction history')
  }
}

export const exportExcel = async (limit = 1000) => {
  try {
    console.log(`📊 Exporting ${limit} records to Excel...`)
    
    // Call the actual API endpoint for Excel export with extended timeout
    const response = await api.get('/api/v1/dataset/export/excel', {
      params: { limit },
      responseType: 'blob',  // Important for file download
      timeout: 90000         // 90 seconds timeout for large Excel generation
    })
    
    // Create download link
    const blob = new Blob([response.data], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    // Generate filename with timestamp
    const timestamp = new Date().toISOString().split('T')[0]
    link.download = `AllerScan-Dataset-${timestamp}.xlsx`
    
    // Trigger download
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // Cleanup
    window.URL.revokeObjectURL(url)
    
    console.log('✅ Excel export completed successfully')
    return { success: true, message: 'Excel file downloaded successfully' }
    
  } catch (error) {
    console.error('❌ Error exporting Excel:', error)
    
    // More specific error messages
    if (error.code === 'ECONNABORTED') {
      throw new Error('Export timeout - File terlalu besar atau server lambat. Coba kurangi jumlah records.')
    }
    
    throw new Error(`Failed to export Excel: ${error.message}`)
  }
}

export const addDatasetEntry = async (data) => {
  try {
    const response = await api.post('/dataset', data)
    return response.data
  } catch (error) {
    console.error('Error adding dataset entry:', error)
    throw new Error('Failed to add dataset entry')
  }
}

export const getDatasetStats = async () => {
  try {
    const response = await api.get('/api/v1/dataset/statistics')
    return response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
    throw new Error('Failed to fetch statistics')
  }
}

// Export service object for backward compatibility
const datasetService = {
  getDataset,
  getAllPredictions,
  getPredictionHistory,
  addDatasetEntry,
  getDatasetStats,
  exportExcel
}

export { datasetService }
export default datasetService
