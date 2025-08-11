import { useState, useCallback } from 'react'

/**
 * Simple form state management hook
 */
export const useFormState = (initialValues) => {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  
  const setValue = useCallback((field, value) => {
    setValues(prev => ({ ...prev, [field]: value }))
  }, [])
  
  const setError = useCallback((field, error) => {
    setErrors(prev => ({ ...prev, [field]: error }))
  }, [])
  
  const reset = useCallback(() => {
    setValues(initialValues)
    setErrors({})
  }, [initialValues])

  return {
    values,
    errors,
    setValue,
    setError,
    reset
  }
}
