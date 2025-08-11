/**
 * Error Boundary & Error Handling Utilities
 * 
 * Comprehensive error handling system untuk production-ready app
 * Mengikuti best practices React error boundaries
 */

import React from 'react'
import { AlertTriangle, RefreshCw, Home } from 'lucide-react'
import Button from '../components/UI/Button'
import Card from '../components/UI/Card'

/**
 * Error Boundary Component
 * Catches JavaScript errors dan shows fallback UI
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null,
      retryCount: 0
    }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    })

    // Log error ke service (bisa ditambahkan Sentry, LogRocket, etc.)
    this.logErrorToService(error, errorInfo)
  }

  logErrorToService = (error, errorInfo) => {
    // Implementasi logging ke external service
    console.group('Error Boundary Caught Error')
    console.error('Error:', error)
    console.error('Error Info:', errorInfo)
    console.error('Stack:', error.stack)
    console.groupEnd()

    // Dapat dintegrasikan dengan service error tracking seperti Sentry
    // Contoh: Sentry.captureException(error, { extra: errorInfo })
  }

  handleRetry = () => {
    this.setState(prevState => ({
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: prevState.retryCount + 1
    }))
  }

  render() {
    if (this.state.hasError) {
      const { error, errorInfo, retryCount } = this.state
      const { fallback: CustomFallback, showDetails = false } = this.props

      // Use custom fallback if provided
      if (CustomFallback) {
        return <CustomFallback 
          error={error} 
          errorInfo={errorInfo} 
          retry={this.handleRetry}
          retryCount={retryCount}
        />
      }

      // Default error UI
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <Card className="max-w-lg w-full">
            <Card.Content className="text-center">
              <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Oops! Terjadi Kesalahan
              </h1>
              <p className="text-gray-600 mb-6">
                Aplikasi mengalami error yang tidak terduga. Tim kami telah diberitahu dan akan memperbaikinya.
              </p>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button
                  onClick={this.handleRetry}
                  icon={RefreshCw}
                  variant="primary"
                  disabled={retryCount >= 3}
                >
                  {retryCount >= 3 ? 'Terlalu Banyak Percobaan' : 'Coba Lagi'}
                </Button>
                
                <Button
                  onClick={() => window.location.href = '/'}
                  icon={Home}
                  variant="outline"
                >
                  Kembali ke Beranda
                </Button>
              </div>

              {showDetails && error && (
                <details className="mt-6 text-left">
                  <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                    Detail Error (untuk debugging)
                  </summary>
                  <div className="mt-2 p-3 bg-gray-100 rounded text-xs font-mono">
                    <div className="text-red-600 font-semibold mb-2">{error.toString()}</div>
                    <pre className="whitespace-pre-wrap text-gray-700">
                      {errorInfo.componentStack}
                    </pre>
                  </div>
                </details>
              )}
            </Card.Content>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

/**
 * Specific Error Fallback Components
 */
export const FormErrorFallback = ({ error, retry }) => (
  <Card>
    <Card.Content className="text-center py-8">
      <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Form Bermasalah
      </h3>
      <p className="text-gray-600 mb-4">
        Terjadi kesalahan saat memproses formulir. Silakan coba lagi.
      </p>
      <Button onClick={retry} icon={RefreshCw} size="sm">
        Muat Ulang Form
      </Button>
    </Card.Content>
  </Card>
)

export const DataErrorFallback = ({ error, retry }) => (
  <Card>
    <Card.Content className="text-center py-8">
      <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Gagal Memuat Data
      </h3>
      <p className="text-gray-600 mb-4">
        Tidak dapat mengambil data dari server. Periksa koneksi internet Anda.
      </p>
      <Button onClick={retry} icon={RefreshCw} size="sm">
        Coba Lagi
      </Button>
    </Card.Content>
  </Card>
)

/**
 * Error Types untuk consistent error handling
 */
export const ErrorTypes = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR', 
  SERVER_ERROR: 'SERVER_ERROR',
  AUTHENTICATION_ERROR: 'AUTHENTICATION_ERROR',
  NOT_FOUND_ERROR: 'NOT_FOUND_ERROR',
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
}

/**
 * Error Handler Utility Functions
 */
export const errorHandler = {
  /**
   * Parse API error response
   */
  parseApiError: (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          return {
            type: ErrorTypes.VALIDATION_ERROR,
            message: data.detail || 'Data yang dikirim tidak valid',
            userMessage: 'Mohon periksa kembali data yang Anda masukkan'
          }
        case 401:
          return {
            type: ErrorTypes.AUTHENTICATION_ERROR,
            message: data.detail || 'Unauthorized',
            userMessage: 'Sesi Anda telah berakhir. Silakan login kembali'
          }
        case 404:
          return {
            type: ErrorTypes.NOT_FOUND_ERROR,
            message: data.detail || 'Resource not found',
            userMessage: 'Data yang diminta tidak ditemukan'
          }
        case 500:
          return {
            type: ErrorTypes.SERVER_ERROR,
            message: data.detail || 'Internal server error',
            userMessage: 'Terjadi kesalahan pada server. Silakan coba lagi'
          }
        default:
          return {
            type: ErrorTypes.SERVER_ERROR,
            message: data.detail || `HTTP ${status}`,
            userMessage: 'Terjadi kesalahan yang tidak terduga'
          }
      }
    } else if (error.request) {
      return {
        type: ErrorTypes.NETWORK_ERROR,
        message: 'No response from server',
        userMessage: 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda'
      }
    } else {
      return {
        type: ErrorTypes.UNKNOWN_ERROR,
        message: error.message,
        userMessage: 'Terjadi kesalahan yang tidak diketahui'
      }
    }
  },

  /**
   * Create user-friendly error message
   */
  getUserMessage: (error) => {
    const parsed = errorHandler.parseApiError(error)
    return parsed.userMessage
  },

  /**
   * Log error dengan context
   */
  logError: (error, context = {}) => {
    const parsed = errorHandler.parseApiError(error)
    
    console.group(`Error: ${parsed.type}`)
    console.error('Message:', parsed.message)
    console.error('User Message:', parsed.userMessage)
    console.error('Context:', context)
    console.error('Original Error:', error)
    console.groupEnd()

    // Dapat dintegrasikan dengan service error tracking
  }
}

/**
 * HOC untuk wrap component dengan error boundary
 */
export const withErrorBoundary = (Component, errorFallback) => {
  const WrappedComponent = (props) => (
    <ErrorBoundary fallback={errorFallback}>
      <Component {...props} />
    </ErrorBoundary>
  )
  
  WrappedComponent.displayName = `withErrorBoundary(${Component.displayName || Component.name})`
  return WrappedComponent
}

export default ErrorBoundary
