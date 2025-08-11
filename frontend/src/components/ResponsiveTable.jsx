import React from 'react'
import { LoadingSkeleton } from './UI/Loading'

/**
 * ResponsiveTable Component
 * 
 * A fully responsive table component that follows DRY principles
 * Features:
 * - Mobile-first responsive design
 * - Column visibility based on screen size
 * - Smooth scrolling for overflow
 * - Accessibility features
 * - Clean documentation
 */

/**
 * ResponsiveTable Component
 * 
 * @param {Array} columns - Array of column configurations with responsive properties
 * @param {Array} data - Array of data rows to display
 * @param {boolean} loading - Loading state indicator
 * @param {string} emptyMessage - Message to show when no data available
 * @param {string} className - Additional CSS classes
 */
const ResponsiveTable = ({ 
  columns = [], 
  data = [], 
  loading = false, 
  emptyMessage = 'Tidak ada data tersedia',
  className = ''
}) => {
  
  /**
   * Get responsive class names for columns based on breakpoint
   * @param {string} responsive - Responsive breakpoint (always, sm, md, lg, xl)
   */
  const getResponsiveClass = (responsive) => {
    switch (responsive) {
      case 'always': return ''
      case 'sm': return 'hidden sm:table-cell'
      case 'md': return 'hidden md:table-cell'
      case 'lg': return 'hidden lg:table-cell'
      case 'xl': return 'hidden xl:table-cell'
      default: return ''
    }
  }

  // Check if table needs horizontal scrolling
  const hasHiddenColumns = columns.some(col => col.responsive !== 'always')

  /**
   * Reusable loading skeleton using unified UI/Loading components
   * This eliminates the need for component-specific loading skeletons
   */
  const LoadingSkeletonRow = () => (
    <tr className="animate-pulse">
      {columns.map((column, index) => (
        <td 
          key={index}
          className={`px-4 py-3 ${getResponsiveClass(column.responsive)} ${column.className || ''}`}
        >
          <LoadingSkeleton className="h-4 w-full rounded" />
        </td>
      ))}
    </tr>
  )

  return (
    <div className={`overflow-x-auto shadow ring-1 ring-black ring-opacity-5 md:rounded-lg ${className}`}>
      {/* Scroll indicator for better UX - only show on mobile when columns are hidden */}
      {hasHiddenColumns && (
        <div className="block sm:hidden bg-gradient-to-r from-blue-50 to-transparent p-3 text-xs text-blue-700 border-b border-blue-100">
          <div className="flex items-center">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
            </svg>
            Geser tabel ke kanan untuk melihat kolom lainnya
          </div>
        </div>
      )}
      <table className="min-w-full divide-y divide-gray-300">
        {/* Table Header */}
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column, index) => (
              <th
                key={index}
                scope="col"
                className={`
                  px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider
                  ${getResponsiveClass(column.responsive)}
                  ${column.className || ''}
                  ${column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''}
                `}
              >
                <div className="flex items-center space-x-1">
                  <span>{column.header}</span>
                  {column.sortable && (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                    </svg>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>

        {/* Table Body */}
        <tbody className="bg-white divide-y divide-gray-200">
          {loading ? (
            // Loading state
            Array.from({ length: 5 }).map((_, index) => (
              <LoadingSkeletonRow key={`skeleton-${index}`} />
            ))
          ) : data.length === 0 ? (
            // Empty state
            <tr>
              <td 
                colSpan={columns.length} 
                className="px-4 py-8 text-center text-gray-500"
              >
                <div className="flex flex-col items-center">
                  <svg 
                    className="w-12 h-12 text-gray-400 mb-4" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth="2" 
                      d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-8V4a2 2 0 00-2-2H7a2 2 0 00-2 2v1m14 0H5"
                    />
                  </svg>
                  <span className="text-lg font-medium">{emptyMessage}</span>
                  <span className="text-sm text-gray-400 mt-1">
                    Data akan muncul setelah memuat dari database
                  </span>
                </div>
              </td>
            </tr>
          ) : (
            // Data rows
            data.map((row, rowIndex) => (
              <tr 
                key={rowIndex}
                className={`
                  hover:bg-gray-50 transition-colors duration-150 ease-in-out
                  ${row.isRecent ? 'bg-blue-50 border-l-4 border-blue-400' : ''}
                  ${row.isFormData ? 'bg-purple-50' : ''}
                `}
              >
                {columns.map((column, colIndex) => (
                  <td
                    key={colIndex}
                    className={`
                      px-4 py-3 whitespace-nowrap text-sm
                      ${getResponsiveClass(column.responsive)}
                      ${column.className || ''}
                    `}
                  >
                    {/* Render cell content */}
                    {column.render ? (
                      column.render(row)
                    ) : column.accessor ? (
                      <span title={String(row[column.accessor])}>
                        {row[column.accessor]}
                      </span>
                    ) : (
                      '-'
                    )}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

export default ResponsiveTable
