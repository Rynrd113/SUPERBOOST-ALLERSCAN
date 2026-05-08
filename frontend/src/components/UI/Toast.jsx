import React, { useEffect } from 'react'
import { CheckCircle, XCircle, X } from 'lucide-react'

const icons = {
  success: <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />,
  error: <XCircle className="w-5 h-5 text-red-500 flex-shrink-0" />,
}

const styles = {
  success: 'bg-white border-green-200 text-green-800',
  error: 'bg-white border-red-200 text-red-800',
}

export const Toast = ({ message, type = 'success', onClose }) => {
  useEffect(() => {
    const t = setTimeout(onClose, 3000)
    return () => clearTimeout(t)
  }, [onClose])

  return (
    <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg text-sm font-medium ${styles[type]}`}>
      {icons[type]}
      <span className="flex-1">{message}</span>
      <button onClick={onClose} className="ml-2 text-slate-400 hover:text-slate-600">
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}

export const ToastContainer = ({ toasts, onClose }) => (
  <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-2 w-full max-w-sm px-4">
    {toasts.map(t => (
      <Toast key={t.id} message={t.message} type={t.type} onClose={() => onClose(t.id)} />
    ))}
  </div>
)

export const useToast = () => {
  const [toasts, setToasts] = React.useState([])

  const show = (message, type = 'success') => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
  }

  const remove = (id) => setToasts(prev => prev.filter(t => t.id !== id))

  return { toasts, show, remove }
}
