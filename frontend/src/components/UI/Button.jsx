import React from 'react'

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  disabled = false,
  loading = false,
  icon: Icon,
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-0.5 active:translate-y-0'
  
  const variants = {
    // Primary - AllerScan Blue
    primary: 'bg-allerscan-500 hover:bg-allerscan-600 text-white focus:ring-allerscan-500 shadow-md hover:shadow-lg',
    
    // Secondary - Neutral Gray
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-900 border border-gray-300 focus:ring-gray-500',
    
    // Outline - AllerScan Blue Outline
    outline: 'border-2 border-allerscan-500 text-allerscan-500 hover:bg-allerscan-500 hover:text-white focus:ring-allerscan-500',
    
    // Ghost - Transparent
    ghost: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:ring-gray-500',
    
    // Semantic Colors
    success: 'bg-success-500 hover:bg-success-600 text-white focus:ring-success-500 shadow-md hover:shadow-lg',
    warning: 'bg-warning-500 hover:bg-warning-600 text-white focus:ring-warning-500 shadow-md hover:shadow-lg',
    danger: 'bg-error-500 hover:bg-error-600 text-white focus:ring-error-500 shadow-md hover:shadow-lg',
    
    // Special variants
    link: 'text-allerscan-500 hover:text-allerscan-600 underline hover:no-underline focus:ring-allerscan-500',
    minimal: 'p-1 hover:bg-gray-100 rounded-md text-gray-500 hover:text-gray-700 focus:ring-gray-500'
  }
  
  const sizes = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl'
  }
  
  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`
  
  return (
    <button 
      className={classes}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" className="opacity-25" />
          <path fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" className="opacity-75" />
        </svg>
      )}
      {Icon && !loading && <Icon className="h-4 w-4 mr-2" />}
      {children}
    </button>
  )
}

export default Button
export { Button }
