/**
 * Reusable Charts Components using Chart.js
 * 
 * Professional, clean, and DRY chart components for data visualization
 * Features:
 * - Consistent styling across all charts
 * - Responsive design
 * - Professional color palette
 * - Accessibility support
 * - Loading and error states
 * 
 * @author SuperBoost AllerScan Team
 * @version 2.0.0 - Clean Architecture
 */

import React from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Doughnut, Bar, Pie } from 'react-chartjs-2'
import { AlertCircle, PieChart as PieChartIcon, BarChart3 } from 'lucide-react'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

// Professional color palette for consistency
const CHART_COLORS = {
  primary: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316'],
  secondary: ['#93C5FD', '#6EE7B7', '#FDE047', '#FCA5A5', '#C4B5FD', '#67E8F9', '#BEF264', '#FDBA74'],
  gradient: [
    'rgba(59, 130, 246, 0.8)',
    'rgba(16, 185, 129, 0.8)',
    'rgba(245, 158, 11, 0.8)',
    'rgba(239, 68, 68, 0.8)',
    'rgba(139, 92, 246, 0.8)',
    'rgba(6, 182, 212, 0.8)',
    'rgba(132, 204, 22, 0.8)',
    'rgba(249, 115, 22, 0.8)'
  ]
}

// Common chart options for consistency
const getCommonOptions = (title) => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 15,
        usePointStyle: true,
        font: {
          size: 12,
          family: 'Inter, system-ui, sans-serif'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#374151',
      borderWidth: 1,
      cornerRadius: 8,
      displayColors: true,
      padding: 12
    },
    title: {
      display: !!title,
      text: title,
      font: {
        size: 16,
        weight: 'bold',
        family: 'Inter, system-ui, sans-serif'
      },
      color: '#1F2937',
      padding: {
        top: 0,
        bottom: 20
      }
    }
  }
})

// Chart wrapper component with consistent styling
const ChartWrapper = ({ children, title, icon: Icon, loading, error, className = '' }) => {
  if (loading) {
    return (
      <div className={`bg-white rounded-lg border p-6 ${className}`}>
        <div className="flex items-center mb-4">
          {Icon && <Icon className="h-5 w-5 text-gray-400 mr-2" />}
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Memuat chart...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={`bg-white rounded-lg border p-6 ${className}`}>
        <div className="flex items-center mb-4">
          <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">{error}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white rounded-lg border shadow-sm p-6 ${className}`}>
      {(title || Icon) && (
        <div className="flex items-center mb-4">
          {Icon && <Icon className="h-5 w-5 text-blue-600 mr-2" />}
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
      )}
      <div className="relative h-64">
        {children}
      </div>
    </div>
  )
}

// Doughnut Chart Component
export const DoughnutChart = ({ 
  data, 
  title, 
  loading = false, 
  error = null,
  className = '',
  showPercentage = true,
  colors = CHART_COLORS.primary
}) => {
  if (!data || data.length === 0) {
    error = 'Tidak ada data untuk ditampilkan'
  }

  const chartData = {
    labels: data?.map(item => item.label || item.name) || [],
    datasets: [{
      data: data?.map(item => item.value || item.count) || [],
      backgroundColor: colors,
      borderColor: colors.map(color => color.replace('0.8', '1')),
      borderWidth: 2,
      hoverBorderWidth: 3,
      hoverBackgroundColor: colors.map(color => color.replace('0.8', '0.9'))
    }]
  }

  const options = {
    ...getCommonOptions(title),
    plugins: {
      ...getCommonOptions().plugins,
      tooltip: {
        ...getCommonOptions().plugins.tooltip,
        callbacks: {
          label: function(context) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0)
            const percentage = ((context.parsed / total) * 100).toFixed(1)
            return showPercentage 
              ? `${context.label}: ${context.parsed} (${percentage}%)`
              : `${context.label}: ${context.parsed}`
          }
        }
      }
    },
    cutout: '50%', // Makes it a doughnut instead of pie
  }

  return (
    <ChartWrapper title={title} icon={PieChartIcon} loading={loading} error={error} className={className}>
      <Doughnut data={chartData} options={options} />
    </ChartWrapper>
  )
}

// Pie Chart Component  
export const PieChart = ({ 
  data, 
  title, 
  loading = false, 
  error = null,
  className = '',
  showPercentage = true,
  colors = CHART_COLORS.primary
}) => {
  if (!data || data.length === 0) {
    error = 'Tidak ada data untuk ditampilkan'
  }

  const chartData = {
    labels: data?.map(item => item.label || item.name) || [],
    datasets: [{
      data: data?.map(item => item.value || item.count) || [],
      backgroundColor: colors,
      borderColor: colors.map(color => color.replace('0.8', '1')),
      borderWidth: 2,
      hoverBorderWidth: 3,
      hoverBackgroundColor: colors.map(color => color.replace('0.8', '0.9'))
    }]
  }

  const options = {
    ...getCommonOptions(title),
    plugins: {
      ...getCommonOptions().plugins,
      tooltip: {
        ...getCommonOptions().plugins.tooltip,
        callbacks: {
          label: function(context) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0)
            const percentage = ((context.parsed / total) * 100).toFixed(1)
            return showPercentage 
              ? `${context.label}: ${context.parsed} (${percentage}%)`
              : `${context.label}: ${context.parsed}`
          }
        }
      }
    }
  }

  return (
    <ChartWrapper title={title} icon={PieChartIcon} loading={loading} error={error} className={className}>
      <Pie data={chartData} options={options} />
    </ChartWrapper>
  )
}

// Bar Chart Component
export const BarChart = ({ 
  data, 
  title, 
  loading = false, 
  error = null,
  className = '',
  colors = CHART_COLORS.primary
}) => {
  if (!data || data.length === 0) {
    error = 'Tidak ada data untuk ditampilkan'
  }

  const chartData = {
    labels: data?.map(item => item.label || item.name) || [],
    datasets: [{
      label: title || 'Data',
      data: data?.map(item => item.value || item.count) || [],
      backgroundColor: colors[0],
      borderColor: colors[0].replace('0.8', '1'),
      borderWidth: 2,
      borderRadius: 4,
      borderSkipped: false,
    }]
  }

  const options = {
    ...getCommonOptions(title),
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          font: {
            size: 12
          }
        }
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          font: {
            size: 12
          }
        }
      }
    }
  }

  return (
    <ChartWrapper title={title} icon={BarChart3} loading={loading} error={error} className={className}>
      <Bar data={chartData} options={options} />
    </ChartWrapper>
  )
}

// Export all components and colors for external use
export { CHART_COLORS, getCommonOptions, ChartWrapper }
export default { DoughnutChart, PieChart, BarChart }
