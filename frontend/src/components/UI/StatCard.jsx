import React from 'react'

/**
 * Reusable StatCard component mengikuti prinsip DRY
 * Menerima props untuk customization tanpa mengubah style dasar
 */
const StatCard = ({ 
  title, 
  value, 
  icon, 
  loading = false,
  className = "",
  containerClass = ""
}) => {
  const IconComponent = icon
  
  return (
    <div className={`p-6 text-center bg-white rounded-3xl shadow-lg border border-slate-200 hover:shadow-xl transition-shadow duration-300 ${containerClass}`}>
      <div className="p-3 bg-gradient-to-r from-blue-100 to-blue-200 rounded-2xl w-fit mx-auto mb-4">
        <IconComponent className="h-8 w-8 text-blue-600" aria-hidden="true" />
      </div>
      <div className={`text-3xl font-bold text-slate-900 mb-2 ${className}`}>
        {loading ? (
          <div className="animate-pulse">
            <div className="h-9 bg-slate-200 rounded w-16 mx-auto"></div>
          </div>
        ) : (
          value
        )}
      </div>
      <div className="text-slate-600 font-medium">{title}</div>
    </div>
  )
}

export default StatCard
