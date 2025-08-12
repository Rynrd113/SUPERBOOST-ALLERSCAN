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
    // Protect dataset page with authentication
    if (page === 'dataset' && !isAuthenticated) {
      alert('Access denied. Admin login required to view dataset.')
      return
    }
    setCurrentPage(page)
  }

  const handleLogin = (credentials) => {
    // Simple authentication logic
    if (credentials.username === 'admin' && credentials.password === 'admin123') {
      setIsAuthenticated(true)
      setCurrentPage('dashboard')
      return true
    }
    return false
  }

  const handleLogout = () => {
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
        return isAuthenticated ? (
          <DatasetPage onNavigate={handleNavigation} detectionHistory={detectionHistory} />
        ) : (
          <div className="text-center py-20">
            <p className="text-gray-600 mb-4">Access denied. Admin login required.</p>
            <button 
              onClick={() => setCurrentPage('login')}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Login as Admin
            </button>
          </div>
        )
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
