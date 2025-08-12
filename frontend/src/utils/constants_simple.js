// API Configuration - use environment variable if available
export const API_BASE_URL = import.meta.env.VITE_API_URL || 
                            import.meta.env.VITE_API_URL_DEV || 
                            'http://localhost:8001'

// Model Information
export const MODEL_INFO = {
  ALGORITHM: 'SVM + AdaBoost',
  ACCURACY: '93.7%',
  SUPPORTED_ALLERGENS_COUNT: 23
}

// UI Constants
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10
}
