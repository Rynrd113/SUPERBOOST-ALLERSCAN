import React from 'react'

const Input = ({ 
  label, 
  id,
  error,
  helpText,
  className = '',
  containerClassName = '',
  ...props 
}) => {
  const inputClasses = `block w-full rounded-lg border px-3 py-2 text-gray-900 placeholder-gray-500 focus:border-allerscan-500 focus:outline-none focus:ring-1 focus:ring-allerscan-500 transition-colors ${
    error 
      ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
      : 'border-gray-300'
  } ${className}`
  
  return (
    <div className={`space-y-1 ${containerClassName}`}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <input
        id={id}
        className={inputClasses}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      {helpText && !error && (
        <p className="text-sm text-gray-500">{helpText}</p>
      )}
    </div>
  )
}

const Select = ({ 
  label, 
  id,
  error,
  helpText,
  children,
  className = '',
  containerClassName = '',
  ...props 
}) => {
  const selectClasses = `block w-full rounded-lg border px-3 py-2 text-gray-900 focus:border-allerscan-500 focus:outline-none focus:ring-1 focus:ring-allerscan-500 transition-colors ${
    error 
      ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
      : 'border-gray-300'
  } ${className}`
  
  return (
    <div className={`space-y-1 ${containerClassName}`}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <select
        id={id}
        className={selectClasses}
        {...props}
      >
        {children}
      </select>
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      {helpText && !error && (
        <p className="text-sm text-gray-500">{helpText}</p>
      )}
    </div>
  )
}

const Textarea = ({ 
  label, 
  id,
  error,
  helpText,
  className = '',
  containerClassName = '',
  rows = 4,
  ...props 
}) => {
  const textareaClasses = `block w-full rounded-lg border px-3 py-2 text-gray-900 placeholder-gray-500 focus:border-allerscan-500 focus:outline-none focus:ring-1 focus:ring-allerscan-500 transition-colors resize-vertical ${
    error 
      ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
      : 'border-gray-300'
  } ${className}`
  
  return (
    <div className={`space-y-1 ${containerClassName}`}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <textarea
        id={id}
        rows={rows}
        className={textareaClasses}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      {helpText && !error && (
        <p className="text-sm text-gray-500">{helpText}</p>
      )}
    </div>
  )
}

const FormGroup = ({ children, className = '' }) => (
  <div className={`space-y-4 ${className}`}>
    {children}
  </div>
)

export { Input, Select, Textarea, FormGroup }
