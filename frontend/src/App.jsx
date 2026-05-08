import React, { useState } from 'react'
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
  const [detectionHistory, setDetectionHistory] = useState([])

  const handleNavigation = (page) => {
    setCurrentPage(page)
  }

  const handleLogin = async (credentials) => {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      })
      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('admin_token', data.access_token)
        setIsAuthenticated(true)
        setCurrentPage('dashboard')
        return true
      }
      return false
    } catch {
      return false
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('admin_token')
    setIsAuthenticated(false)
    setCurrentPage('dashboard')
  }

  const handleDetectionResult = (result) => {
    setDetectionHistory(prev => [result, ...prev])
  }

  // Show login page for dataset access
  if (currentPage === 'login') {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoginPage 
          onLogin={handleLogin} 
          onBack={() => setCurrentPage('dashboard')} 
        />
      </div>
    )
  }

  const renderPage = () => {
    switch(currentPage) {
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigation} />
      case 'dataset':
        return <DatasetPage onNavigate={handleNavigation} isAuthenticated={isAuthenticated} />
      case 'form':
        return <FormPage onNavigate={handleNavigation} onDetectionResult={handleDetectionResult} />
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
