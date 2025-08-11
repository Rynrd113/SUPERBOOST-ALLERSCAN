import { useState } from 'react'

/**
 * Simple loading state hook
 */
export const useLoadingStates = (initialState = false) => {
  const [loading, setLoading] = useState(initialState)
  
  return {
    loading,
    setLoading
  }
}

export default useLoadingStates
