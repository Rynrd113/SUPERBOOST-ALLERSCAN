import React from 'react'
import { AlertTriangle } from 'lucide-react'
import Button from './Button'

const ConfirmModal = ({ message, onConfirm, onCancel }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
    <div className="absolute inset-0 bg-black/40" onClick={onCancel} />
    <div className="relative bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm">
      <div className="flex items-start gap-4">
        <div className="p-2 bg-red-100 rounded-full flex-shrink-0">
          <AlertTriangle className="w-5 h-5 text-red-600" />
        </div>
        <div>
          <h3 className="font-semibold text-slate-900 mb-1">Konfirmasi Hapus</h3>
          <p className="text-sm text-slate-600">{message}</p>
        </div>
      </div>
      <div className="flex justify-end gap-3 mt-6">
        <Button variant="outline" size="sm" onClick={onCancel}>
          Batal
        </Button>
        <Button
          size="sm"
          onClick={onConfirm}
          className="bg-red-600 hover:bg-red-700 text-white border-transparent"
        >
          Hapus
        </Button>
      </div>
    </div>
  </div>
)

export default ConfirmModal
