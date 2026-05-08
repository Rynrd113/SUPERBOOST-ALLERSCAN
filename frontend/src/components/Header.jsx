import { Shield, User, LogIn, LogOut, Database, Search, Lock } from 'lucide-react'

const Header = ({ currentPage, onNavigate, isAuthenticated, onLogout, onLogin }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Shield, requiresAuth: false },
    { id: 'form', label: 'Deteksi Alergen', icon: Search, requiresAuth: false },
    { id: 'dataset', label: 'Dataset', icon: Database, requiresAuth: false },
  ]

  return (
    <header className="bg-gradient-to-r from-allerscan-700 to-allerscan-800 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center p-1">
                <img 
                  src="/logo/Logo SuperBoost-AllerScan.png" 
                  alt="SuperBoost AllerScan Logo"
                  className="w-full h-full object-contain"
                />
              </div>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-white">
                SUPERBOOST ALLERSCAN
              </h1>
              <p className="text-xs text-allerscan-100">
                Data Mining - Machine Learning
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = currentPage === item.id
              const isDisabled = item.requiresAuth && !isAuthenticated
              
              return (
                <button
                  key={item.id}
                  onClick={() => !isDisabled && onNavigate(item.id)}
                  className={`
                    flex items-center px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200
                    ${isActive
                      ? 'bg-white text-allerscan-700 shadow-sm'
                      : isDisabled
                        ? 'text-allerscan-300 cursor-not-allowed'
                        : 'text-allerscan-100 hover:text-white hover:bg-white/10'
                    }
                  `}
                  disabled={isDisabled}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {item.label}
                  {isDisabled && <Lock className="ml-1 w-3 h-3" />}
                </button>
              )
            })}
          </nav>

          {/* Auth Section */}
          <div className="flex items-center space-x-3">
            {isAuthenticated ? (
              <>
                <div className="hidden sm:flex items-center space-x-2 bg-white/10 px-3 py-1.5 rounded-lg">
                  <User className="w-4 h-4 text-white" />
                  <span className="text-sm font-medium text-white">Admin</span>
                </div>
                <button
                  onClick={onLogout}
                  className="flex items-center px-3 py-1.5 text-sm font-medium text-white hover:bg-white/10 rounded-lg transition-colors duration-200"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            ) : (
              <button
                onClick={onLogin}
                className="flex items-center px-3 py-1.5 text-sm font-medium text-white hover:bg-white/10 rounded-lg transition-colors duration-200"
              >
                <LogIn className="w-4 h-4 mr-2" />
                <span className="hidden sm:inline">Login</span>
              </button>
            )}
          </div>

        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-allerscan-600 py-2">
          <div className="flex items-center justify-around">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = currentPage === item.id
              const isDisabled = item.requiresAuth && !isAuthenticated
              
              return (
                <button
                  key={item.id}
                  onClick={() => !isDisabled && onNavigate(item.id)}
                  className={`
                    flex flex-col items-center px-2 py-1 rounded-lg text-xs transition-all duration-200
                    ${isActive
                      ? 'text-white'
                      : isDisabled
                        ? 'text-allerscan-300'
                        : 'text-allerscan-200 hover:text-white'
                    }
                  `}
                  disabled={isDisabled}
                >
                  <Icon className="w-5 h-5 mb-1" />
                  <span>{item.label}</span>
                  {isDisabled && <Lock className="w-3 h-3 mt-0.5" />}
                </button>
              )
            })}
          </div>
        </div>

      </div>
    </header>
  )
}

export default Header
