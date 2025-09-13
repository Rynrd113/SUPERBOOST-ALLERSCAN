import React, { useState } from 'react';
import { Lock, User, Eye, EyeOff, LogIn, ArrowLeft, Shield, Sparkles } from 'lucide-react';
import Button from './UI/Button';
import LogoSection from './UI/LogoSection';

const LoginPage = ({ onLogin, onBack, isLoading }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  // Simple form handler
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user types
    if (loginError) {
      setLoginError(null);
    }
  };

  // Submit handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.username.trim() || !formData.password.trim()) {
      setLoginError('Username dan password wajib diisi');
      return;
    }
    
    try {
      await onLogin(formData);
    } catch (err) {
      const errorMessage = err.message || 'Login gagal. Periksa username dan password Anda.';
      setLoginError(errorMessage);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        
        {/* Navigation Button */}
        <div className="mb-8">
          <Button
            onClick={onBack}
            variant="secondary"
            className="bg-white hover:bg-slate-50 border-2 border-slate-200 hover:border-slate-300 shadow-sm rounded-2xl"
          >
            <ArrowLeft className="h-5 w-5 mr-3" />
            Kembali ke Dashboard
          </Button>
        </div>

        {/* Page Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-4 bg-gradient-to-r from-blue-600 to-blue-700 rounded-3xl shadow-xl mb-6">
            <Lock className="h-8 w-8 text-white mr-3" />
            <h1 className="text-3xl font-bold text-white">Admin Login</h1>
          </div>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Akses sistem administrasi untuk mengelola 
            <span className="font-semibold text-blue-600"> aplikasi SuperBoost-Allerscan</span>
          </p>
        </div>

        {/* Login Form */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-2xl shadow-lg border overflow-hidden">
            
            {/* Form Header */}
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6">
              <div className="text-center">
                <div className="flex justify-center space-x-4 mb-4">
                  <img 
                    src="/logo/Logo SuperBoost-AllerScan.png" 
                    alt="AllerScan Logo" 
                    className="h-10 object-contain"
                  />
                  <img 
                    src="/logo/Logo Unkartur.png" 
                    alt="Unkartur Logo" 
                    className="h-10 object-contain"
                  />
                </div>
                <h2 className="text-2xl font-bold text-white mb-2">Form Login Admin</h2>
                <p className="text-slate-300">Masukkan kredensial untuk mengakses sistem</p>
              </div>
            </div>

            <div className="p-8">
              <form onSubmit={handleSubmit} className="space-y-8">
                {/* Username Field */}
                <div className="space-y-3">
                  <label htmlFor="username" className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                    Username *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                      <User className="h-5 w-5 text-slate-400" />
                    </div>
                    <input
                      type="text"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleInputChange}
                      className="w-full pl-12 pr-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      placeholder="Masukkan username admin"
                      required
                    />
                  </div>
                </div>

                {/* Password Field */}
                <div className="space-y-3">
                  <label htmlFor="password" className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                    Password *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-slate-400" />
                    </div>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="w-full pl-12 pr-16 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      placeholder="Masukkan password admin"
                      required
                    />
                    <Button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      variant="minimal"
                      size="sm"
                      className="absolute inset-y-0 right-0 pr-4 flex items-center h-full hover:bg-transparent"
                    >
                      {showPassword ? (
                        <EyeOff className="h-5 w-5 text-slate-400 hover:text-slate-600" />
                      ) : (
                        <Eye className="h-5 w-5 text-slate-400 hover:text-slate-600" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Login Error */}
                {loginError && (
                  <div className="bg-gradient-to-r from-red-50 to-red-100 border border-red-200 rounded-2xl p-4">
                    <div className="flex items-center">
                      <div className="p-2 bg-red-600 rounded-full mr-4">
                        <Lock className="h-4 w-4 text-white" />
                      </div>
                      <div>
                        <h4 className="text-red-800 font-semibold">Login Gagal</h4>
                        <p className="text-red-700 text-sm">{loginError}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Login Button */}
                <div className="flex justify-center pt-6">
                  <Button
                    type="submit"
                    disabled={isLoading || !formData.username.trim() || !formData.password.trim()}
                    loading={isLoading}
                    size="lg"
                    className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-12 py-4 text-lg font-bold rounded-2xl shadow-2xl hover:shadow-blue-500/25 transform hover:scale-105 transition-all duration-300"
                  >
                    <LogIn className="h-6 w-6 mr-3" />
                    {isLoading ? 'Memproses Login...' : 'Login ke Sistem'}
                  </Button>
                </div>
              </form>

              {/* Default Credentials Info - Removed */}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-slate-200">
          <div className="text-center">
            <div className="flex justify-center space-x-6 mb-4">
              <img 
                src="/logo/Logo Bima-Dikti.png" 
                alt="Bima Dikti Logo" 
                className="h-10 object-contain opacity-70"
              />
              <img 
                src="/logo/Logo Diktisaintek Berdampak.png" 
                alt="Diktisaintek Logo" 
                className="h-10 object-contain opacity-70"
              />
            </div>
            <p className="text-slate-500 text-sm">
              Powered by <span className="font-semibold">Universitas Nasional Karangturi</span> • 
              Supported by <span className="font-semibold">Direktorat Penelitian dan Pengabdian kepada Masyarakat (DPPM) - Kementrian Pendidikan Tinggi, Sains dan Teknologi, Direktorat Jendral Riset dan Pengembangan</span>
            </p>
            <p className="text-slate-400 text-xs mt-2">
              © 2025 SuperBoost-AllerScan Aplikasi Deteksi Alergen Berbasis Data Mining & Machine Learning
            </p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;
