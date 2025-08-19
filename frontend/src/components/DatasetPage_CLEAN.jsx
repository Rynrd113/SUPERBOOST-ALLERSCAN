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

// Helper functions
const formatConfidence = (confidence) => {
  if (!confidence) return '0.0%'
  
  const numericValue = typeof confidence === 'string' ? 
    parseFloat(confidence) : confidence
  
  if (numericValue <= 1) {
    return `${(numericValue * 100).toFixed(1)}%`
  } else {
    return `${numericValue.toFixed(1)}%`
  }
}

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

  // Data loading function
  const loadData = useCallback(async (page = 1, pageSize = 20) => {
    try {
      setLoading(true)
      setError(null)
      
      const params = {
        page,
        page_size: pageSize
      }
      
      if (searchTerm.trim()) {
        params.search = searchTerm.trim()
      }
      
      const response = await api.get('/api/v1/dataset/', { params })
      
      if (response.data && response.data.data) {
        setData(response.data.data)
        setTotalItems(response.data.pagination?.total || response.data.data.length)
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
      setStatistics(response.data.statistics || null)
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

  const handleDelete = async (id) => {
    if (!window.confirm('Apakah Anda yakin ingin menghapus data ini?')) {
      return
    }
    
    try {
      await deletePrediction(id)
      await loadData(currentPage, itemsPerPage)
      await loadStatistics()
      alert('Data berhasil dihapus')
    } catch (error) {
      console.error('Error deleting data:', error)
      alert('Gagal menghapus data')
    }
  }

  const handleExport = async () => {
    try {
      setIsExporting(true)
      await exportToExcel()
      alert('Data berhasil diekspor ke Excel')
    } catch (error) {
      console.error('Error exporting data:', error)
      alert('Gagal mengekspor data')
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
          icon={Database}
          title="Total Data"
          value={statistics.total_records || 0}
          color="blue"
        />
        <DatasetStatCard
          icon={AlertCircle}
          title="Terdeteksi Alergen"
          value={statistics.allergen_detected || 0}
          color="red"
        />
        <DatasetStatCard
          icon={BarChart3}
          title="Rata-rata Confidence"
          value={statistics.avg_confidence ? `${(statistics.avg_confidence * 100).toFixed(1)}%` : '0.0%'}
          color="green"
        />
        <DatasetStatCard
          icon={Table}
          title="Unique Alergen"
          value={statistics.unique_allergens || 0}
          color="purple"
        />
      </div>
    )
  }

  const renderCharts = () => {
    if (!statistics?.allergen_distribution || !statistics?.confidence_distribution) {
      return null
    }

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Distribusi Alergen</h3>
          <DoughnutChart data={statistics.allergen_distribution} />
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Distribusi Confidence</h3>
          <PieChart data={statistics.confidence_distribution} />
        </div>
      </div>
    )
  }

  const renderPagination = () => {
    const totalPages = Math.ceil(totalItems / itemsPerPage)
    if (totalPages <= 1) return null

    return (
      <div className="flex justify-center items-center mt-6 space-x-2">
        <Button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage <= 1}
          variant="outline"
          size="sm"
        >
          <ChevronLeft className="w-4 h-4" />
        </Button>
        
        <span className="text-sm text-gray-600">
          Halaman {currentPage} dari {totalPages}
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
    )
  }

  const columns = [
    {
      header: 'ID',
      accessor: 'id',
      className: 'text-center'
    },
    {
      header: 'Bahan Makanan',
      accessor: 'food_ingredient',
      className: 'font-medium'
    },
    {
      header: 'Alergen',
      accessor: 'allergens',
      render: (value) => (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          value === 'Tidak terdeteksi' || value === 'tidak terdeteksi'
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          {formatAllergens(value)}
        </span>
      )
    },
    {
      header: 'Confidence',
      accessor: 'confidence',
      render: (value) => (
        <span className="font-mono text-sm">
          {formatConfidence(value)}
        </span>
      ),
      className: 'text-center'
    },
    {
      header: 'Aksi',
      accessor: 'actions',
      render: (_, row) => (
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
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dataset Management</h1>
              <p className="text-gray-600 mt-1">Kelola data hasil prediksi alergen</p>
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
                className="bg-green-600 hover:bg-green-700"
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
        <div className="bg-white rounded-lg shadow-md p-6">
          {/* Search Bar */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Cari bahan makanan..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                <span className="text-red-700">{error}</span>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center py-8">
              <LoaderIcon className="w-8 h-8 animate-spin text-blue-500" />
              <span className="ml-2 text-gray-600">Memuat data...</span>
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
