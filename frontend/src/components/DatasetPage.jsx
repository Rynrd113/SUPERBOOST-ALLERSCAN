import React, { useState, useEffect, useCallback } from 'react'
import {
  Database,
  Search,
  Table,
  BarChart3,
  AlertCircle,
  Loader as LoaderIcon,
  Trash2,
  RefreshCw,
  Download,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

import api, { deletePrediction, exportToExcel } from '../services/api'
import { DoughnutChart, PieChart } from './UI/Charts'
import ResponsiveTable from './ResponsiveTable'
import Button from './UI/Button'
import DatasetStatCard from './UI/DatasetStatCard'
import { ToastContainer, useToast } from './UI/Toast'
import ConfirmModal from './UI/ConfirmModal'

// Helper functions
const formatAllergens = (allergens) => {
  if (!allergens || allergens === 'tidak terdeteksi') return 'Tidak terdeteksi'
  if (typeof allergens === 'string') {
    try {
      const parsed = JSON.parse(allergens)
      if (Array.isArray(parsed)) {
        return parsed.map(a => typeof a === 'object' ? a.allergen : a).join(', ')
      }
    } catch {
      return allergens
    }
  }
  if (Array.isArray(allergens)) {
    return allergens.map(a => typeof a === 'object' ? a.allergen : a).join(', ')
  }
  return allergens
}

// Main component
const DatasetPage = () => {
  // State management
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(20)
  const [totalItems, setTotalItems] = useState(0)
  const [searchTerm, setSearchTerm] = useState('')
  const [statistics, setStatistics] = useState(null)
  const [isExporting, setIsExporting] = useState(false)
  const [confirmDelete, setConfirmDelete] = useState(null)
  const { toasts, show: showToast, remove: removeToast } = useToast()

  // Data loading function
  const loadData = useCallback(async (page = 1, pageSize = 20) => {
    try {
      setLoading(true)
      setError(null)

      const params = {
        page,
        limit: pageSize,        // fix: was page_size
        include_stats: false
      }

      if (searchTerm.trim()) {
        params.search = searchTerm.trim()
      }

      const response = await api.get('/api/v1/dataset/predictions', { params })  // fix: correct endpoint

      const responseData = response.data?.data
      if (responseData) {
        setData(responseData.predictions || [])                          // fix: extract predictions array
        setTotalItems(responseData.pagination?.total_items || 0)        // fix: correct field name
        setCurrentPage(page)
      } else {
        setData([])
        setTotalItems(0)
      }
    } catch (error) {
      console.error('Error loading data:', error)
      setError('Gagal memuat data. Silakan coba lagi.')
      setData([])
      setTotalItems(0)
    } finally {
      setLoading(false)
    }
  }, [searchTerm])

  // Statistics loading function
  const loadStatistics = useCallback(async () => {
    try {
      const response = await api.get('/api/v1/dataset/statistics')
      setStatistics(response.data.data || null)   // fix: was response.data.statistics (tidak ada)
    } catch (error) {
      console.error('Error loading statistics:', error)
      setStatistics(null)
    }
  }, [])

  // Effects
  useEffect(() => {
    loadData(1, itemsPerPage)
  }, [loadData, itemsPerPage])

  useEffect(() => {
    loadStatistics()
  }, [loadStatistics])

  // Event handlers
  const handleSearch = () => {
    setCurrentPage(1)
    loadData(1, itemsPerPage)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const handlePageChange = (page) => {
    loadData(page, itemsPerPage)
  }

  const handleRefresh = () => {
    setSearchTerm('')
    setCurrentPage(1)
    loadData(1, itemsPerPage)
    loadStatistics()
  }

  const handleDelete = (id) => {
    setConfirmDelete(id)
  }

  const confirmDeleteAction = async () => {
    const id = confirmDelete
    setConfirmDelete(null)
    try {
      await deletePrediction(id)
      await loadData(currentPage, itemsPerPage)
      await loadStatistics()
      showToast('Data berhasil dihapus', 'success')
    } catch (error) {
      console.error('Error deleting data:', error)
      showToast('Gagal menghapus data', 'error')
    }
  }

  const handleExport = async () => {
    try {
      setIsExporting(true)
      const blob = await exportToExcel()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `superboost_allerscan_dataset_${new Date().toISOString().slice(0,10)}.xlsx`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error exporting data:', error)
      showToast('Gagal mengekspor data', 'error')
    } finally {
      setIsExporting(false)
    }
  }

  // Render helpers
  const renderStatistics = () => {
    if (!statistics) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          {[...Array(4)].map((_, index) => (
            <DatasetStatCard key={index} loading={true} />
          ))}
        </div>
      )
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <DatasetStatCard
          icon={<Database className="w-8 h-8" />}
          title="Total Data"
          value={statistics.overview?.total_predictions || 0}
          bgColor="bg-blue-50"
          textColor="text-blue-700"
        />
        <DatasetStatCard
          icon={<AlertCircle className="w-8 h-8" />}
          title="Terdeteksi Alergen"
          value={statistics.detection_breakdown?.detected_count || 0}
          bgColor="bg-red-50"
          textColor="text-red-700"
        />
        <DatasetStatCard
          icon={<BarChart3 className="w-8 h-8" />}
          title="Akurasi Model"
          value={statistics.model_info?.accuracy || '0%'}
          bgColor="bg-green-50"
          textColor="text-green-700"
        />
        <DatasetStatCard
          icon={<Table className="w-8 h-8" />}
          title="Alergen Terdeteksi"
          value={statistics.chart_data?.allergens_distribution?.length || 0}
          bgColor="bg-purple-50"
          textColor="text-purple-700"
        />
      </div>
    )
  }

  const renderCharts = () => {
    const allergenDist = statistics?.chart_data?.allergens_distribution
    const detectionPie = statistics?.chart_data?.detection_pie

    if (!allergenDist?.length && !detectionPie?.length) {
      return null
    }

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {allergenDist?.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-100">
            <h3 className="text-lg font-semibold mb-4 text-slate-900">Distribusi Alergen</h3>
            <DoughnutChart data={allergenDist} />
          </div>
        )}
        {detectionPie?.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-100">
            <h3 className="text-lg font-semibold mb-4 text-slate-900">Hasil Deteksi</h3>
            <PieChart data={detectionPie} />
          </div>
        )}
      </div>
    )
  }

  const renderPagination = () => {
    const totalPages = Math.ceil(totalItems / itemsPerPage)
    if (totalPages <= 1) return null

    const from = (currentPage - 1) * itemsPerPage + 1
    const to = Math.min(currentPage * itemsPerPage, totalItems)

    return (
      <div className="flex flex-col sm:flex-row justify-between items-center mt-6 gap-3">
        <span className="text-sm text-slate-500">
          Menampilkan <span className="font-semibold text-slate-700">{from}–{to}</span> dari{' '}
          <span className="font-semibold text-slate-700">{totalItems}</span> data
        </span>

        <div className="flex items-center space-x-2">
          <Button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage <= 1}
            variant="outline"
            size="sm"
          >
            <ChevronLeft className="w-4 h-4" />
          </Button>

          <span className="text-sm text-slate-600 px-2">
            {currentPage} / {totalPages}
          </span>

          <Button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage >= totalPages}
            variant="outline"
            size="sm"
          >
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>
      </div>
    )
  }

  const columns = [
    {
      header: 'No',
      render: (row) => <span className="text-slate-500">{row.display_id || row.id}</span>,
      className: 'text-center w-12'
    },
    {
      header: 'Nama Produk',
      render: (row) => (
        <span className="font-medium text-slate-900">{row.product_name || row.nama_produk || '-'}</span>
      )
    },
    {
      header: 'Bahan Utama',
      render: (row) => <span className="text-slate-700">{row.bahan_utama || '-'}</span>,
      responsive: 'md'
    },
    {
      header: 'Pemanis',
      render: (row) => <span className="text-slate-700">{row.pemanis || '-'}</span>,
      responsive: 'lg'
    },
    {
      header: 'Lemak/Minyak',
      render: (row) => <span className="text-slate-700">{row.lemak_minyak || '-'}</span>,
      responsive: 'lg'
    },
    {
      header: 'Penyedap Rasa',
      render: (row) => <span className="text-slate-700">{row.penyedap_rasa || '-'}</span>,
      responsive: 'xl'
    },
    {
      header: 'Alergen',
      render: (row) => {
        const allergens = row.detected_allergens || row.predicted_allergens
        const isDetected = (row.allergen_count || 0) > 0
        if (!isDetected) return <span className="text-slate-400">—</span>
        return <span className="text-red-700 text-xs font-medium">{formatAllergens(allergens)}</span>
      },
      responsive: 'sm'
    },
    {
      header: 'Prediksi',
      render: (row) => {
        const isDetected = (row.allergen_count || 0) > 0
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium whitespace-nowrap ${
            isDetected ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
          }`}>
            {isDetected ? 'Mengandung Alergen' : 'Tidak Mengandung Alergen'}
          </span>
        )
      },
      responsive: 'sm',
      className: 'text-center'
    },
    {
      header: 'Tanggal',
      render: (row) => {
        if (!row.created_at) return <span className="text-slate-400">—</span>
        const d = new Date(row.created_at)
        const date = d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })
        const time = d.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
        return (
          <div className="text-xs text-slate-600">
            <div className="font-medium">{date}</div>
            <div className="text-slate-400">{time}</div>
          </div>
        )
      },
      responsive: 'md',
      className: 'text-center'
    },
    {
      header: 'Aksi',
      render: (row) => (
        <Button
          onClick={() => handleDelete(row.id)}
          variant="outline"
          size="sm"
          className="text-red-600 border-red-200 hover:bg-red-50"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      ),
      className: 'text-center'
    }
  ]

  // Main render
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 py-8 px-4">
      {confirmDelete && (
        <ConfirmModal
          message="Data ini akan dihapus permanen dan tidak bisa dikembalikan."
          onConfirm={confirmDeleteAction}
          onCancel={() => setConfirmDelete(null)}
        />
      )}
      <ToastContainer toasts={toasts} onClose={removeToast} />
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-slate-100">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Dataset Management</h1>
              <p className="text-slate-600 mt-1">Data hasil prediksi alergen pengguna</p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                onClick={handleRefresh}
                variant="outline"
                disabled={loading}
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>

              <Button
                onClick={handleExport}
                disabled={isExporting || data.length === 0}
                className="bg-green-600 hover:bg-green-700 text-white"
              >
                <Download className={`w-4 h-4 mr-2 ${isExporting ? 'animate-spin' : ''}`} />
                {isExporting ? 'Exporting...' : 'Export Excel'}
              </Button>
            </div>
          </div>

        </div>

        {/* Statistics Cards */}
        {renderStatistics()}

        {/* Charts */}
        {renderCharts()}

        {/* Search and Table */}
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-100">
          {/* Search Bar */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Cari bahan makanan..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full pl-10 pr-4 py-2 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-allerscan-500/20 focus:border-allerscan-500 transition-all duration-200"
                />
              </div>
            </div>
            <Button onClick={handleSearch} disabled={loading}>
              <Search className="w-4 h-4 mr-2" />
              Cari
            </Button>
          </div>

          {/* Error State */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                <span className="text-red-700">{error}</span>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center py-8">
              <LoaderIcon className="w-8 h-8 animate-spin text-allerscan-500" />
              <span className="ml-2 text-slate-600">Memuat data...</span>
            </div>
          )}

          {/* Table */}
          {!loading && !error && (
            <>
              <ResponsiveTable
                data={data}
                columns={columns}
                emptyMessage="Tidak ada data yang ditemukan"
              />
              {renderPagination()}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default DatasetPage
