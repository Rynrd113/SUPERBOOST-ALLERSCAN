import axios from 'axios'

// Base API configuration
const API_BASE_URL = 'http://localhost:8001'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,  // Increased to 15 seconds default
  headers: {
    'Content-Type': 'application/json',
  }
})

// Simple error handler
const handleApiError = (error) => {
  if (error.code === 'ECONNABORTED') {
    throw new Error('Request timeout - Server tidak merespons')
  }
  
  if (error.code === 'ERR_NETWORK') {
    throw new Error('Network error - Pastikan backend server berjalan')
  }
  
  if (error.response) {
    const { status, data } = error.response
    throw new Error(data.detail || `HTTP ${status} error`)
  }
  
  throw new Error('Terjadi kesalahan koneksi')
}

// API functions
export const predictAllergen = async (data) => {
  try {
    const response = await api.post('/api/v1/predict/', data)
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

export const addDataset = async (data) => {
  try {
    const response = await api.post('/api/v1/dataset/predictions', data)
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

export const getDataset = async (page = 1, pageSize = 10) => {
  try {
    const response = await api.get('/api/v1/dataset/predictions', {
      params: { page, page_size: pageSize }
    })
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

export const getDatasetStats = async () => {
  try {
    const response = await api.get('/api/v1/dataset/statistics')
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

export const getBackendStatus = async () => {
  try {
    const response = await api.get('/api/v1/health')
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

// Alias for backward compatibility
export const checkHealth = getBackendStatus

// Delete prediction
export const deletePrediction = async (predictionId) => {
  try {
    const response = await api.delete(`/api/v1/dataset/predictions/${predictionId}`)
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

// Export to Excel
export const exportToExcel = async (limit = 1000) => {
  try {
    const response = await api.get('/api/v1/dataset/export/excel', {
      params: { limit },
      responseType: 'blob',  // Important for downloading files
      timeout: 90000         // 90 seconds timeout for Excel generation (increased)
    })
    return response.data
  } catch (error) {
    console.error('❌ Export Excel API Error:', error)
    handleApiError(error)
  }
}

// Auth functions
export const login = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials)
    return response.data
  } catch (error) {
    handleApiError(error)
  }
}

export default api
