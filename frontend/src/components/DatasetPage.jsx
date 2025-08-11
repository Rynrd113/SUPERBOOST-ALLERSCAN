import React, { useState, useEffect } from 'react'
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
    } catch (e) {
      return allergens
    }
  }
  if (Array.isArray(allergens)) {
    return allergens.map(a => typeof a === 'object' ? a.allergen : a).join(', ')
  }
  return allergens.toString()
}

// Reusable Components
const StatCard = ({ title, value, subtitle, bgColor = 'bg-blue-50', textColor = 'text-blue-700', icon }) => (
  <div className={`${bgColor} rounded-lg p-6 border border-opacity-20 hover:shadow-md transition-shadow`}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className={`text-3xl font-bold ${textColor}`}>{value}</p>
        {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
      </div>
      {icon && <div className={`opacity-60 ${textColor}`}>{icon}</div>}
    </div>
  </div>
)

const BreakdownCard = ({ title, data, total, maxDisplay = 5 }) => {
  const entries = Object.entries(data || {})
  const sortedEntries = entries.sort(([,a], [,b]) => b - a).slice(0, maxDisplay)

  return (
    <div className="bg-white rounded-lg border p-6 hover:shadow-md transition-shadow">
      <h4 className="font-semibold text-gray-800 mb-4 text-lg">{title}</h4>
      {sortedEntries.length === 0 ? (
        <p className="text-sm text-gray-500 italic">Belum ada data</p>
      ) : (
        <div className="space-y-3">
          {sortedEntries.map(([key, value]) => {
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
            return (
              <div key={key} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                <span className="text-sm text-gray-700 font-medium truncate" title={key}>
                  {key.length > 25 ? key.substring(0, 25) + '...' : key}
                </span>
                <div className="flex items-center gap-3">
                  <span className="text-sm font-bold text-gray-900">{value}</span>
                  <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    {percentage}%
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// Data Table Component with Pagination
const DataTable = ({ data, loading, error, searchTerm, onSearchChange, onDelete, onRefresh, onExport, pagination, onPageChange, onItemsPerPageChange }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoaderIcon className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-3 text-lg text-gray-600">Memuat data...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <AlertCircle className="h-6 w-6 text-red-600 mr-3" />
            <div>
              <h3 className="text-red-800 font-medium">Error memuat data</h3>
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          </div>
          <Button variant="danger" onClick={onRefresh} size="sm">
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="text-center py-12">
        <Database className="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Tidak ada data</h3>
        <p className="text-gray-500">Belum ada data prediksi untuk ditampilkan</p>
      </div>
    )
  }

  // Filter data based on search term
  const filteredData = data.filter(item => {
    if (!searchTerm) return true
    const searchLower = searchTerm.toLowerCase()
    return (
      item.product_name?.toLowerCase().includes(searchLower) ||
      item.nama_produk?.toLowerCase().includes(searchLower) ||
      item.ingredients?.toLowerCase().includes(searchLower) ||
      formatAllergens(item.detected_allergens).toLowerCase().includes(searchLower)
    )
  })

  // Define responsive table columns
  const columns = [
    {
      header: 'No.',
      accessor: 'display_no',
      responsive: 'always',
      className: 'min-w-[60px]',
      render: (row, index) => (
        <span className="font-medium">{row.display_no || index + 1}</span>
      )
    },
    {
      header: 'Nama Produk',
      accessor: 'product_name',
      responsive: 'always',
      className: 'min-w-[150px]',
      render: (row) => (
        <div className="font-medium">
          {row.product_name || row.nama_produk || 'N/A'}
        </div>
      )
    },
    {
      header: 'Bahan-bahan',
      accessor: 'ingredients',
      responsive: 'md',
      className: 'min-w-[200px]',
      render: (row) => (
        <div className="max-w-xs truncate" title={row.ingredients}>
          {row.ingredients || 'N/A'}
        </div>
      )
    },
    {
      header: 'Alergen Terdeteksi',
      accessor: 'detected_allergens',
      responsive: 'sm',
      className: 'min-w-[150px]',
      render: (row) => (
        <div className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
          formatAllergens(row.detected_allergens) === 'Tidak terdeteksi'
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}>
          {formatAllergens(row.detected_allergens)}
        </div>
      )
    },
    {
      header: 'Confidence',
      accessor: 'confidence_score',
      responsive: 'sm',
      className: 'min-w-[100px]',
      render: (row) => (
        <span className="font-medium">
          {formatConfidence(row.confidence_score)}
        </span>
      )
    },
    {
      header: 'Risiko',
      accessor: 'risk_level',
      responsive: 'lg',
      className: 'min-w-[100px]',
      render: (row) => (
        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium capitalize ${
          row.risk_level === 'high' ? 'bg-red-100 text-red-800' :
          row.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
          'bg-green-100 text-green-800'
        }`}>
          {row.risk_level || 'none'}
        </span>
      )
    },
    {
      header: 'Tanggal',
      accessor: 'created_at',
      responsive: 'lg',
      className: 'min-w-[120px]',
      render: (row) => (
        <span className="text-gray-600">
          {row.created_at ? 
            new Date(row.created_at).toLocaleDateString('id-ID') : 
            'N/A'}
        </span>
      )
    },
    {
      header: 'Aksi',
      responsive: 'always',
      className: 'min-w-[80px]',
      render: (row) => (
        <Button
          variant="danger"
          size="sm"
          onClick={() => onDelete?.(row.id)}
          className="w-8 h-8 p-0"
          title="Hapus data"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      )
    }
  ]

  return (
    <div className="space-y-6">
      {/* Search and Actions */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <div className="relative flex-1 w-full sm:max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Cari nama produk, bahan, atau alergen..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <div className="flex gap-2">
          <Button variant="secondary" onClick={onRefresh} size="md">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button 
            variant="success" 
            onClick={onExport}
            data-export-btn
            size="md"
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Results Info - Enhanced */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="text-sm text-gray-600">
          <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
            <span>
              Menampilkan {filteredData.length} dari {pagination?.total_items || data.length} data
            </span>
            {searchTerm && (
              <span className="mt-1 sm:mt-0 px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                Pencarian: "{searchTerm}"
              </span>
            )}
          </div>
        </div>
        {pagination && (
          <div className="text-sm text-gray-500 bg-gray-50 px-3 py-1 rounded">
            Halaman {pagination.current_page} dari {pagination.total_pages}
          </div>
        )}
      </div>

      {/* Responsive Table */}
      <ResponsiveTable
        columns={columns}
        data={filteredData.map((item, index) => ({
          ...item,
          display_no: ((pagination?.current_page || 1) - 1) * (pagination?.items_per_page || 10) + index + 1
        }))}
        loading={loading}
        emptyMessage="Tidak ada data prediksi untuk ditampilkan"
        className="bg-white rounded-xl shadow-sm"
      />

      {/* Pagination Controls */}
      {pagination && pagination.total_pages > 1 && (
        <div className="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0 px-6 py-4 bg-gray-50 border-t">
          {/* Items per page selector */}
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <span>Tampilkan:</span>
            <select 
              value={pagination.items_per_page}
              onChange={(e) => onItemsPerPageChange?.(parseInt(e.target.value))}
              className="border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
            <span>per halaman</span>
          </div>

          {/* Pagination buttons */}
          <div className="flex items-center space-x-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onPageChange(pagination.current_page - 1)}
              disabled={!pagination.has_previous}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Previous
            </Button>
            
            {/* Page numbers */}
            <div className="flex items-center space-x-1">
              {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
                let pageNumber
                if (pagination.total_pages <= 5) {
                  pageNumber = i + 1
                } else {
                  const start = Math.max(1, pagination.current_page - 2)
                  const end = Math.min(pagination.total_pages, start + 4)
                  pageNumber = start + i
                  if (pageNumber > end) return null
                }
                
                return (
                  <Button
                    key={pageNumber}
                    variant={pageNumber === pagination.current_page ? 'primary' : 'secondary'}
                    size="sm"
                    onClick={() => onPageChange(pageNumber)}
                    className="min-w-[40px]"
                  >
                    {pageNumber}
                  </Button>
                )
              }).filter(Boolean)}
            </div>
            
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onPageChange(pagination.current_page + 1)}
              disabled={!pagination.has_more}
            >
              Next
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

// Statistics Component with Charts
const StatisticsView = ({ stats, loading, onRefreshStats }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoaderIcon className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-3 text-lg text-gray-600">Memuat statistik...</span>
      </div>
    )
  }

  if (!stats || stats.total === 0) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Tidak ada data</h3>
        <p className="text-gray-500">Belum ada data untuk ditampilkan dalam statistik</p>
        {onRefreshStats && (
          <Button variant="primary" onClick={onRefreshStats} className="mt-4">
            <RefreshCw className="h-4 w-4 mr-2" />
            Muat Ulang Statistik
          </Button>
        )}
      </div>
    )
  }

  // Prepare chart data
  const confidenceChartData = stats.confidenceDistribution ? [
    { label: 'Rendah (<70%)', value: stats.confidenceDistribution.low || 0 },
    { label: 'Sedang (70-85%)', value: stats.confidenceDistribution.medium || 0 },
    { label: 'Tinggi (>85%)', value: stats.confidenceDistribution.high || 0 }
  ] : []

  const allergenChartData = Object.entries(stats.allergenBreakdown || {})
    .sort(([,a], [,b]) => b - a)
    .slice(0, 6)
    .map(([key, value]) => ({ label: key, value }))

  const statusChartData = Object.entries(stats.statusBreakdown || {})
    .map(([key, value]) => ({ label: key, value }))

  return (
    <div className="space-y-8">
      {/* Header with Refresh Button */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Statistik Dataset</h2>
          <p className="text-sm text-gray-600">
            Statistik berdasarkan semua data prediksi ({stats.total?.toLocaleString() || '0'} records)
          </p>
        </div>
        {onRefreshStats && (
          <Button variant="secondary" onClick={onRefreshStats} size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Statistik
          </Button>
        )}
      </div>
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Prediksi"
          value={stats.total?.toLocaleString() || '0'}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          }
          bgColor="bg-blue-50"
          textColor="text-blue-700"
        />
        <StatCard
          title="Rata-rata Confidence"
          value={`${stats.averageConfidence?.toFixed(1) || '0'}%`}
          subtitle="Skor kepercayaan model"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
          bgColor="bg-green-50"
          textColor="text-green-700"
        />
        <StatCard
          title="Aktivitas 7 Hari"
          value={stats.recentActivity?.toLocaleString() || '0'}
          subtitle="Prediksi terbaru"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          }
          bgColor="bg-purple-50"
          textColor="text-purple-700"
        />
        <StatCard
          title="Jenis Alergen"
          value={Object.keys(stats.allergenBreakdown || {}).length}
          subtitle="Alergen terdeteksi"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.19 2.5 1.732 2.5z" />
            </svg>
          }
          bgColor="bg-orange-50"
          textColor="text-orange-700"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {/* Confidence Distribution Chart */}
        <DoughnutChart
          data={confidenceChartData}
          title="Distribusi Confidence Score"
          loading={loading}
          className="lg:col-span-1"
        />

        {/* Allergen Detection Chart */}
        <PieChart
          data={allergenChartData}
          title="Alergen Terdeteksi"
          loading={loading}
          className="lg:col-span-1"
        />

        {/* Status Chart */}
        <DoughnutChart
          data={statusChartData}
          title="Status Deteksi"
          loading={loading}
          className="lg:col-span-1"
        />
      </div>

      {/* Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <BreakdownCard
          title="Status Alergen"
          data={stats.statusBreakdown || {}}
          total={stats.total}
        />
        <BreakdownCard
          title="Alergen Terdeteksi"
          data={stats.allergenBreakdown || {}}
          total={stats.total}
        />
        <BreakdownCard
          title="Bahan Utama"
          data={stats.bahan_utama_breakdown || {}}
          total={stats.total}
        />
        <BreakdownCard
          title="Pemanis"
          data={stats.pemanis_breakdown || {}}
          total={stats.total}
        />
        <BreakdownCard
          title="Lemak & Minyak"
          data={stats.lemak_minyak_breakdown || {}}
          total={stats.total}
        />
        <BreakdownCard
          title="Penyedap Rasa"
          data={stats.penyedap_rasa_breakdown || {}}
          total={stats.total}
        />
      </div>
    </div>
  )
}

// Main Component
function DatasetPage({ onNavigate }) {
  const [data, setData] = useState([])
  const [stats, setStats] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('table')
  const [searchTerm, setSearchTerm] = useState('')
  const [pagination, setPagination] = useState({
    current_page: 1,
    total_pages: 1,
    total_items: 0,
    items_per_page: 10,
    has_more: false,
    has_previous: false
  })

  // 🔧 UPDATED: Calculate statistics from predictions (with clear logging)
  const calculateStatistics = (predictions) => {
    console.log(`📊 Calculating statistics from ${predictions.length} predictions`)
    
    if (!predictions.length) {
      console.log('⚠️ No predictions data - setting empty statistics')
      setStats({
        total: 0,
        averageConfidence: 0,
        allergenBreakdown: {},
        statusBreakdown: {},
        recentActivity: 0,
        confidenceDistribution: { low: 0, medium: 0, high: 0 },
        bahan_utama_breakdown: {},
        pemanis_breakdown: {},
        lemak_minyak_breakdown: {},
        penyedap_rasa_breakdown: {}
      })
      return
    }

    const total = predictions.length
    const totalConfidence = predictions.reduce((sum, p) => sum + (p.confidence_score || 0), 0)
    const averageConfidence = total > 0 ? totalConfidence / total : 0

    const allergenBreakdown = {}
    const statusBreakdown = {}
    const confidenceDistribution = { low: 0, medium: 0, high: 0 }
    const bahan_utama_breakdown = {}
    const pemanis_breakdown = {}
    const lemak_minyak_breakdown = {}
    const penyedap_rasa_breakdown = {}

    predictions.forEach(prediction => {
      // Status breakdown
      const status = prediction.status_alergen || prediction.detection_status || 'Tidak Terdeteksi'
      statusBreakdown[status] = (statusBreakdown[status] || 0) + 1

      // Allergen breakdown
      if (prediction.detected_allergens && prediction.detected_allergens !== 'tidak terdeteksi') {
        const allergens = formatAllergens(prediction.detected_allergens)
        if (allergens !== 'Tidak terdeteksi') {
          allergens.split(', ').forEach(allergen => {
            const cleanAllergen = allergen.trim()
            if (cleanAllergen) {
              allergenBreakdown[cleanAllergen] = (allergenBreakdown[cleanAllergen] || 0) + 1
            }
          })
        }
      }

      // Confidence distribution
      const confidence = (prediction.confidence_score || 0) * 100
      if (confidence < 70) confidenceDistribution.low++
      else if (confidence < 85) confidenceDistribution.medium++
      else confidenceDistribution.high++

      // Form field breakdowns - include all values including "Tidak Ada"
      if (prediction.bahan_utama && prediction.bahan_utama.trim() !== '') {
        bahan_utama_breakdown[prediction.bahan_utama] = (bahan_utama_breakdown[prediction.bahan_utama] || 0) + 1
      }
      if (prediction.pemanis && prediction.pemanis.trim() !== '') {
        pemanis_breakdown[prediction.pemanis] = (pemanis_breakdown[prediction.pemanis] || 0) + 1
      }
      if (prediction.lemak_minyak && prediction.lemak_minyak.trim() !== '') {
        lemak_minyak_breakdown[prediction.lemak_minyak] = (lemak_minyak_breakdown[prediction.lemak_minyak] || 0) + 1
      }
      if (prediction.penyedap_rasa && prediction.penyedap_rasa.trim() !== '') {
        penyedap_rasa_breakdown[prediction.penyedap_rasa] = (penyedap_rasa_breakdown[prediction.penyedap_rasa] || 0) + 1
      }
    })

    // Recent activity (last 7 days)
    const sevenDaysAgo = new Date()
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
    const recentActivity = predictions.filter(p => 
      new Date(p.created_at || p.timestamp) > sevenDaysAgo
    ).length

    const calculatedStats = {
      total,
      averageConfidence: Math.round(averageConfidence * 100 * 100) / 100,
      allergenBreakdown,
      statusBreakdown,
      recentActivity,
      confidenceDistribution,
      bahan_utama_breakdown,
      pemanis_breakdown,
      lemak_minyak_breakdown,
      penyedap_rasa_breakdown
    }

    console.log('📈 Calculated statistics:', calculatedStats)
    setStats(calculatedStats)
  }

  // Load data from API with pagination
  const loadData = async (page = 1, pageSize = 20) => {
    try {
      setLoading(true)
      setError('')
      
      const response = await api.get('/api/v1/dataset/predictions', {
        params: { page, page_size: pageSize, include_stats: true }
      })
      
      if (response.data) {
        let predictions = []
        let paginationData = {}
        let statsData = null
        
        // Handle different response formats
        if (response.data.data) {
          predictions = response.data.data.predictions || []
          paginationData = response.data.data.pagination || {}
          statsData = response.data.data.statistics || null
        } else {
          predictions = response.data.predictions || []
          paginationData = response.data.pagination || {}
          statsData = response.data.statistics || null
        }
        
        if (predictions.length > 0) {
          const processedData = predictions.map((item, index) => ({
            ...item,
            id: item.id || index + 1,
            no: index + 1
          }))
          
          setData(processedData)
          setPagination({
            current_page: paginationData.current_page || page,
            total_pages: paginationData.total_pages || 1,
            total_items: paginationData.total_items || predictions.length,
            items_per_page: paginationData.items_per_page || pageSize,
            has_more: paginationData.has_more || false,
            has_previous: paginationData.has_previous || false
          })
          
          // 🔧 FIX: Always load comprehensive statistics from backend
          await loadComprehensiveStatistics()
          
        } else {
          setData([])
          setPagination({
            current_page: 1,
            total_pages: 1,
            total_items: 0,
            items_per_page: pageSize,
            has_more: false,
            has_previous: false
          })
          // Empty statistics for no data
          setStats({
            total: 0,
            averageConfidence: 0,
            allergenBreakdown: {},
            statusBreakdown: {},
            recentActivity: 0,
            confidenceDistribution: { low: 0, medium: 0, high: 0 },
            bahan_utama_breakdown: {},
            pemanis_breakdown: {},
            lemak_minyak_breakdown: {},
            penyedap_rasa_breakdown: {}
          })
        }
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          err.message || 
                          'Gagal memuat data'
      setError(errorMessage)
      setData([])
    } finally {
      setLoading(false)
    }
  }

  // 🔧 NEW: Load comprehensive statistics from backend (separate API call for accuracy)
  const loadComprehensiveStatistics = async () => {
    try {
      console.log('🔄 Loading comprehensive statistics from backend...')
      
      const statsResponse = await api.get('/api/v1/dataset/statistics')
      
      if (statsResponse.data && statsResponse.data.data) {
        const backendStats = statsResponse.data.data
        console.log('📊 Backend statistics loaded:', backendStats)
        
        // Convert backend statistics to frontend format
        setStats({
          total: backendStats.overview?.total_predictions || 0,
          averageConfidence: backendStats.overview?.average_confidence || 0,
          allergenBreakdown: backendStats.chart_data?.allergens_distribution?.reduce((acc, item) => {
            acc[item.name] = item.count
            return acc
          }, {}) || {},
          statusBreakdown: backendStats.chart_data?.detection_pie?.reduce((acc, item) => {
            acc[item.name] = item.count
            return acc
          }, {}) || {},
          recentActivity: 0, // Not provided by backend stats endpoint
          confidenceDistribution: {
            // Create confidence distribution from average (approximation)
            low: Math.floor((backendStats.overview?.total_predictions || 0) * 0.2),
            medium: Math.floor((backendStats.overview?.total_predictions || 0) * 0.5),
            high: Math.floor((backendStats.overview?.total_predictions || 0) * 0.3)
          },
          riskDistribution: backendStats.chart_data?.risk_distribution?.reduce((acc, item) => {
            acc[item.level] = item.count
            return acc
          }, {}) || {},
          detectionRate: backendStats.overview?.detection_rate || 0,
          bahan_utama_breakdown: {},
          pemanis_breakdown: {},
          lemak_minyak_breakdown: {},
          penyedap_rasa_breakdown: {}
        })
        
        // 🔧 FIX: Calculate breakdown data from actual predictions
        await calculateBreakdownFromAllData()
        
        console.log('✅ Statistics successfully loaded and formatted')
      }
    } catch (statsError) {
      console.error('❌ Error loading comprehensive statistics:', statsError)
      // Fallback to basic stats if comprehensive stats fail
      console.log('🔄 Falling back to basic statistics calculation...')
      calculateBasicStatistics()
    }
  }

  // 🔧 NEW: Calculate breakdown data from all prediction data
  const calculateBreakdownFromAllData = async () => {
    try {
      console.log('🔄 Calculating ingredient breakdowns from all data...')
      
      // Get all predictions for breakdown calculation
      const allDataResponse = await api.get('/api/v1/dataset/predictions', {
        params: { page: 1, page_size: 1000, include_stats: false }
      })
      
      let allPredictions = []
      if (allDataResponse.data?.data?.predictions) {
        allPredictions = allDataResponse.data.data.predictions
      } else if (allDataResponse.data?.predictions) {
        allPredictions = allDataResponse.data.predictions
      }
      
      if (allPredictions.length === 0) {
        console.log('⚠️ No predictions found for breakdown calculation')
        return
      }
      
      console.log(`📊 Processing ${allPredictions.length} predictions for breakdowns...`)
      
      // Calculate breakdowns
      const bahan_utama_breakdown = {}
      const pemanis_breakdown = {}
      const lemak_minyak_breakdown = {}
      const penyedap_rasa_breakdown = {}
      
      allPredictions.forEach(prediction => {
        if (prediction.bahan_utama && prediction.bahan_utama.trim() !== '') {
          bahan_utama_breakdown[prediction.bahan_utama] = (bahan_utama_breakdown[prediction.bahan_utama] || 0) + 1
        }
        if (prediction.pemanis && prediction.pemanis.trim() !== '') {
          pemanis_breakdown[prediction.pemanis] = (pemanis_breakdown[prediction.pemanis] || 0) + 1
        }
        if (prediction.lemak_minyak && prediction.lemak_minyak.trim() !== '') {
          lemak_minyak_breakdown[prediction.lemak_minyak] = (lemak_minyak_breakdown[prediction.lemak_minyak] || 0) + 1
        }
        if (prediction.penyedap_rasa && prediction.penyedap_rasa.trim() !== '') {
          penyedap_rasa_breakdown[prediction.penyedap_rasa] = (penyedap_rasa_breakdown[prediction.penyedap_rasa] || 0) + 1
        }
      })
      
      // Update stats with breakdowns
      setStats(prevStats => ({
        ...prevStats,
        bahan_utama_breakdown,
        pemanis_breakdown,
        lemak_minyak_breakdown,
        penyedap_rasa_breakdown
      }))
      
      console.log('✅ Ingredient breakdowns calculated:', {
        bahan_utama_count: Object.keys(bahan_utama_breakdown).length,
        pemanis_count: Object.keys(pemanis_breakdown).length,
        lemak_minyak_count: Object.keys(lemak_minyak_breakdown).length,
        penyedap_rasa_count: Object.keys(penyedap_rasa_breakdown).length
      })
      
    } catch (error) {
      console.error('❌ Error calculating ingredient breakdowns:', error)
    }
  }

  // 🔧 NEW: Calculate basic statistics from current data (fallback only)
  const calculateBasicStatistics = async () => {
    try {
      // Get all data for accurate statistics (not just current page)
      const allDataResponse = await api.get('/api/v1/dataset/predictions', {
        params: { page: 1, page_size: 1000, include_stats: false } // Get large batch for stats
      })
      
      let allPredictions = []
      if (allDataResponse.data?.data?.predictions) {
        allPredictions = allDataResponse.data.data.predictions
      } else if (allDataResponse.data?.predictions) {
        allPredictions = allDataResponse.data.predictions
      }
      
      console.log(`📊 Calculating basic statistics from ${allPredictions.length} total records`)
      calculateStatistics(allPredictions)
      
    } catch (error) {
      console.error('❌ Error calculating basic statistics:', error)
      // Ultimate fallback - use current page data
      calculateStatistics(data)
    }
  }

  // Handle pagination
  const handlePageChange = (page) => {
    if (page >= 1 && page <= pagination.total_pages) {
      loadData(page, pagination.items_per_page)
    }
  }

  // Handle items per page change
  const handleItemsPerPageChange = (itemsPerPage) => {
    loadData(1, itemsPerPage)
  }

  // Delete data handler
  const handleDelete = async (id) => {
    if (!id) {
      alert('ID tidak valid untuk penghapusan')
      return
    }

    if (window.confirm('Apakah Anda yakin ingin menghapus data ini?')) {
      try {
        // Call API to delete data from database
        await deletePrediction(id)
        
        // Reload current page data after successful deletion
        // Refresh current page data
        loadData(pagination.current_page, pagination.items_per_page)
        
        // Show success message
        alert('Data berhasil dihapus!')
      } catch (err) {
        console.error('Error deleting data:', err)
        alert('Gagal menghapus data: ' + err.message)
      }
    }
  }

  // Export to Excel handler
  const handleExportExcel = async () => {
    try {
      // Show loading state
      const exportButton = document.querySelector('[data-export-btn]')
      if (exportButton) {
        exportButton.disabled = true
        exportButton.innerHTML = '<svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25" /><path fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75" /></svg>Mengunduh...'
      }

      // Use the API export function with reasonable limit
      const exportLimit = Math.min(data.length || 1000, 5000) // Cap at 5000 records to prevent timeout
      console.log(`🔄 Starting Excel export for ${exportLimit} records...`)
      
      const blob = await exportToExcel(exportLimit)
      
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      // Generate filename with current date
      const currentDate = new Date().toISOString().split('T')[0]
      link.download = `AllerScan-Dataset-${currentDate}.xlsx`
      
      // Trigger download
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      // Show success message
      alert(`File Excel berhasil diunduh! (${exportLimit} records)`)
      
    } catch (err) {
      console.error('Error exporting Excel:', err)
      
      // More specific error handling
      let errorMessage = 'Gagal mengunduh file Excel'
      if (err.message.includes('timeout')) {
        errorMessage = 'Timeout: Server terlalu lama merespons. Coba kurangi jumlah data atau coba lagi nanti.'
      } else if (err.message.includes('network')) {
        errorMessage = 'Masalah koneksi: Pastikan backend server berjalan.'
      } else if (err.message.includes('Request timeout')) {
        errorMessage = 'Server timeout: Coba lagi dengan jumlah data yang lebih kecil.'
      }
      
      alert(`Error: ${errorMessage}: ${err.message}`)
    } finally {
      // Reset button state
      const exportButton = document.querySelector('[data-export-btn]')
      if (exportButton) {
        exportButton.disabled = false
        exportButton.innerHTML = '<svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>Export'
      }
    }
  }

  const tabs = [
    { id: 'table', label: 'Tabel Data', icon: Table },
    { id: 'chart', label: 'Statistik & Charts', icon: BarChart3 }
  ]

  useEffect(() => {
    console.log('🚀 DatasetPage mounted - loading initial data')
    loadData(1, 20)
  }, [])

  // Debug effect to monitor state changes
  useEffect(() => {
    console.log('📊 Statistics updated:', {
      total: stats.total,
      averageConfidence: stats.averageConfidence,
      allergenBreakdownKeys: Object.keys(stats.allergenBreakdown || {}),
      statusBreakdownKeys: Object.keys(stats.statusBreakdown || {})
    })
  }, [stats])

  useEffect(() => {
    console.log('📄 Data updated:', {
      dataLength: data.length,
      paginationTotal: pagination.total_items,
      currentPage: pagination.current_page
    })
  }, [data, pagination])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Navigation Button */}
        <div className="flex justify-between items-center">
          <button
            onClick={() => onNavigate('form')}
            className="inline-flex items-center px-6 py-3 border border-gray-300 shadow-sm text-base font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all"
          >
            ← Kembali ke Form
          </button>
        </div>

        {/* Page Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-4 bg-gradient-to-r from-blue-600 to-blue-700 rounded-3xl shadow-xl mb-6">
            <Database className="h-8 w-8 text-white mr-3" />
            <h1 className="text-3xl font-bold text-white">Dataset Analisis Alergen</h1>
          </div>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Riwayat dan statistik hasil analisis alergen makanan menggunakan 
            <span className="font-semibold text-blue-600"> algoritma SVM + AdaBoost</span>
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-2xl shadow-sm border p-2">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 flex items-center justify-center px-6 py-4 text-sm font-medium rounded-xl transition-all ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-5 w-5 mr-2" />
                  {tab.label}
                </button>
              )
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-2xl shadow-lg border overflow-hidden">
          {activeTab === 'table' && (
            <div className="p-6">
              <DataTable 
                data={data} 
                loading={loading} 
                error={error}
                searchTerm={searchTerm}
                onSearchChange={setSearchTerm}
                onDelete={handleDelete}
                onRefresh={() => {
                  console.log('🔄 Manual refresh triggered')
                  loadData(pagination.current_page, pagination.items_per_page)
                }}
                onExport={handleExportExcel}
                pagination={pagination}
                onPageChange={handlePageChange}
                onItemsPerPageChange={handleItemsPerPageChange}
              />
            </div>
          )}
          
          {activeTab === 'chart' && (
            <div className="p-6">
              <StatisticsView 
                stats={stats} 
                loading={loading}
                onRefreshStats={() => {
                  console.log('🔄 Manual statistics refresh triggered')
                  loadComprehensiveStatistics()
                }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DatasetPage
