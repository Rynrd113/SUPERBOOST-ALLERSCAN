import React from 'react'

/**
 * DatasetStatCard - Komponen statistik khusus untuk halaman dataset
 * Berbeda dengan StatCard umum karena memiliki layout dan style yang berbeda
 */
const DatasetStatCard = ({ 
  title, 
  value, 
  subtitle, 
  bgColor = 'bg-blue-50', 
  textColor = 'text-blue-700', 
  icon,
  className = ""
}) => (
  <div className={`${bgColor} rounded-lg p-6 border border-opacity-20 hover:shadow-md transition-shadow ${className}`}>
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

export default DatasetStatCard
