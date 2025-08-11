import React from 'react'

const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  }

  return (
    <div className={`animate-spin rounded-full border-2 border-gray-300 border-t-blue-600 ${sizeClasses[size]} ${className}`} />
  )
}

const LoadingSkeleton = ({ className = '' }) => (
  <div className={`bg-gray-200 animate-pulse rounded ${className}`} />
)

// Simple skeleton components for DatasetPage
const SkeletonStats = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    {Array.from({ length: 4 }).map((_, index) => (
      <div key={index} className="bg-white p-6 rounded-lg border border-gray-200">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    ))}
  </div>
)

const SkeletonTable = ({ rows = 5, columns = 4 }) => (
  <div className="bg-white rounded-lg border border-gray-200">
    {/* Table Header */}
    <div className="px-6 py-3 border-b border-gray-200 bg-gray-50">
      <div className="grid grid-cols-6 gap-4">
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="h-4 bg-gray-200 animate-pulse rounded"></div>
        ))}
      </div>
    </div>
    
    {/* Table Rows */}
    <div className="divide-y divide-gray-200">
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="px-6 py-4">
          <div className="grid grid-cols-6 gap-4">
            {Array.from({ length: 6 }).map((_, colIndex) => (
              <div key={colIndex} className="h-4 bg-gray-200 animate-pulse rounded"></div>
            ))}
          </div>
        </div>
      ))}
    </div>
  </div>
)

export { LoadingSpinner, LoadingSkeleton, SkeletonStats, SkeletonTable }
