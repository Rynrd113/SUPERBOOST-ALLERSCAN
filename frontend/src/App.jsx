import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import FormPage from './components/FormPage'
import DatasetPage from './components/DatasetPage'
import LoginPage from './components/LoginPage'
import BackendStatus from './components/BackendStatus'
import Footer from './components/Footer'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoginLoading, setIsLoginLoading] = useState(false)

  // Verify existing token on first load
  useEffect(() => {
    const token = localStorage.getItem('admin_token')
    if (!token) return
    fetch('/api/v1/auth/verify', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (res.ok) setIsAuthenticated(true)
        else localStorage.removeItem('admin_token')
      })
      .catch(() => localStorage.removeItem('admin_token'))
  }, [])

  // Auto-logout when token expires (fired by api.js interceptor)
  useEffect(() => {
    const handleExpired = () => {
      setIsAuthenticated(false)
      setCurrentPage('login')
    }
    window.addEventListener('auth:expired', handleExpired)
    return () => window.removeEventListener('auth:expired', handleExpired)
  }, [])

  const handleNavigation = (page) => {
    if (page === 'dataset' && !isAuthenticated) {
      setCurrentPage('login')
      return
    }
    setCurrentPage(page)
  }

  const handleLogin = async (credentials) => {
    try {
      setIsLoginLoading(true)
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      })
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('admin_token', data.access_token)
        setIsAuthenticated(true)
        setCurrentPage('dataset')
        return true
      }
      return false
    } catch {
      return false
    } finally {
      setIsLoginLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('admin_token')
    setIsAuthenticated(false)
    setCurrentPage('dashboard')
  }


  if (currentPage === 'login') {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoginPage
          onLogin={handleLogin}
          onBack={() => setCurrentPage('dashboard')}
          isLoading={isLoginLoading}
        />
      </div>
    )
  }

  const renderPage = () => {
    switch(currentPage) {
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigation} />
      case 'dataset':
        return <DatasetPage onNavigate={handleNavigation} />
      case 'form':
        return <FormPage onNavigate={handleNavigation} />
      default:
        return <Dashboard onNavigate={handleNavigation} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        currentPage={currentPage}
        onNavigate={handleNavigation}
        isAuthenticated={isAuthenticated}
        onLogout={handleLogout}
        onLogin={() => setCurrentPage('login')}
      />

      <main className="pb-20">
        {renderPage()}
      </main>

      <Footer />
      <BackendStatus />
    </div>
  )
}

export default App
