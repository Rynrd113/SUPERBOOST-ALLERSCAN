import { useState, useEffect } from 'react'
import { Wifi, WifiOff, AlertTriangle, CheckCircle } from 'lucide-react'
import { getBackendStatus } from '../services/api'
import Button from './UI/Button'

const StatusBadge = ({ status, text }) => {
  const statusStyles = {
    online: 'bg-green-100 text-green-800 border-green-200',
    offline: 'bg-red-100 text-red-800 border-red-200',
    loading: 'bg-amber-100 text-amber-800 border-amber-200',
    error: 'bg-red-100 text-red-800 border-red-200'
  }

  const getIcon = () => {
    switch (status) {
      case 'online':
        return <CheckCircle className="h-3 w-3" />
      case 'offline':
        return <WifiOff className="h-3 w-3" />
      case 'loading':
        return <AlertTriangle className="h-3 w-3" />
      default:
        return <AlertTriangle className="h-3 w-3" />
    }
  }

  return (
    <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium border rounded-full ${statusStyles[status] || statusStyles.error}`}>
      {getIcon()}
      {text}
    </span>
  )
}

const BackendStatus = () => {
  const [status, setStatus] = useState('loading')
  const [lastChecked, setLastChecked] = useState(null)
  const [isVisible, setIsVisible] = useState(true)

  const checkBackendStatus = async () => {
    try {
      const health = await getBackendStatus()
      if (health.status === 'operational' || health.status === 'healthy') {
        setStatus('healthy')
      } else {
        setStatus('warning')
      }
    } catch (error) {
      console.log('Backend connection error (expected during startup):', error.message)
      setStatus('error')
    } finally {
      setLastChecked(new Date())
    }
  }

  useEffect(() => {
    checkBackendStatus()
    
    // Check every 60 seconds during heavy operations, 30 seconds normally
    const interval = setInterval(checkBackendStatus, 60000)
    
    return () => clearInterval(interval)
  }, [])

  if (!isVisible) return null

  const statusConfig = {
    healthy: {
      icon: <CheckCircle className="h-4 w-4" />,
      text: 'API Connected',
      color: 'text-green-600'
    },
    warning: {
      icon: <AlertTriangle className="h-4 w-4" />,
      text: 'API Warning',
      color: 'text-amber-600'
    },
    error: {
      icon: <WifiOff className="h-4 w-4" />,
      text: 'API Disconnected',
      color: 'text-red-600'
    },
    loading: {
      icon: <Wifi className="h-4 w-4" />,
      text: 'Checking...',
      color: 'text-blue-600'
    }
  }

  const config = statusConfig[status]

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-3">
        <div className="flex items-center space-x-2">
          <div className={config.color}>
            {config.icon}
          </div>
          <StatusBadge status={status} text={config.text} />
          <Button
            onClick={() => setIsVisible(false)}
            variant="secondary"
            size="sm"
            className="text-gray-400 hover:text-gray-600 ml-2 p-1"
          >
            ×
          </Button>
        </div>
        {lastChecked && (
          <div className="text-xs text-gray-500 mt-1">
            Last checked: {lastChecked.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  )
}

export default BackendStatus
