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
            size="sm"
            className="bg-white hover:bg-slate-50 border-2 border-slate-200 hover:border-slate-300 shadow-sm rounded-2xl"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Kembali ke Home
          </Button>
        </div>

        {/* Page Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-4 bg-gradient-to-r from-allerscan-600 to-allerscan-700 rounded-3xl shadow-xl mb-6">
            <Shield className="h-8 w-8 text-white mr-3" />
            <h1 className="text-3xl font-bold text-white">Admin Login</h1>
          </div>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Akses dashboard administrator untuk mengelola aplikasi 
            <span className="font-semibold text-allerscan-600"> SuperBoost-Allerscan</span>
          </p>
          <div className="mt-4 inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            <Sparkles className="h-4 w-4 mr-2" />
            Data Mining - Machine Learning
          </div>
        </div>

        {/* Main Login Card */}
        <div className="max-w-md mx-auto">
          <div className="bg-white rounded-3xl shadow-2xl border-0 overflow-hidden">
            {/* Card Header */}
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6">
              <div className="flex items-center justify-center mb-4">
                <div className="p-3 bg-allerscan-600 rounded-full">
                  <Lock className="h-8 w-8 text-white" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-white text-center mb-2">Login Administrator</h2>
              <p className="text-slate-300 text-center">Masukkan kredensial admin Anda</p>
            </div>

            {/* Login Form */}
            <div className="p-8">
              <form onSubmit={handleSubmit} className="space-y-8">
                
                {/* Username Field */}
                <div className="space-y-3">
                  <label htmlFor="username" className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                    Username Administrator
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
                      className="w-full pl-12 pr-4 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-allerscan-500 focus:ring-4 focus:ring-allerscan-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      placeholder="Masukkan username admin"
                      required
                    />
                  </div>
                </div>

                {/* Password Field */}
                <div className="space-y-3">
                  <label htmlFor="password" className="block text-sm font-bold text-slate-700 uppercase tracking-wide">
                    Password Administrator
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
                      className="w-full pl-12 pr-16 py-4 text-lg border-2 border-slate-200 rounded-2xl focus:border-allerscan-500 focus:ring-4 focus:ring-allerscan-500/20 transition-all duration-300 bg-slate-50 focus:bg-white"
                      placeholder="Masukkan password admin"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-4 flex items-center"
                    >
                      {showPassword ? (
                        <EyeOff className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                      ) : (
                        <Eye className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Login Error */}
                {loginError && (
                  <div className="p-4 bg-red-50 border-2 border-red-200 rounded-2xl">
                    <p className="text-sm text-red-700 font-medium text-center">{loginError}</p>
                  </div>
                )}

                {/* Login Button */}
                <div className="flex justify-center pt-6">
                  <Button
                    type="submit"
                    size="lg"
                    disabled={isLoading || !formData.username.trim() || !formData.password.trim()}
                    className="bg-gradient-to-r from-allerscan-600 to-allerscan-700 hover:from-allerscan-700 hover:to-allerscan-800 text-white px-12 py-4 text-lg font-bold rounded-2xl shadow-2xl hover:shadow-allerscan-500/25 transform hover:scale-105 transition-all duration-300"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                        Memproses Login...
                      </>
                    ) : (
                      <>
                        <LogIn className="h-5 w-5 mr-3" />
                        Login Administrator
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </div>

            {/* Default Credentials Card - Removed */}
          </div>
        </div>

        {/* University Branding Footer */}
        <div className="text-center mt-16">
          <LogoSection variant="compact" className="mb-6" />
          <div className="space-y-2 text-slate-500">
            <p className="text-lg font-semibold">
              Powered by <span className="text-allerscan-600">Universitas Nasional Karangturi</span>
            </p>
            <div className="flex items-center justify-center space-x-4 text-sm">
              <span>Supported by <span className="font-semibold">Direktorat Penelitian dan Pengabdian kepada Masyarakat (DPPM)</span></span>
              <span>•</span>
              <span><span className="font-semibold">Kementrian Pendidikan Tinggi, Sains dan Teknologi</span></span>
              <span>•</span>
              <span><span className="font-semibold">Direktorat Jendral Riset dan Pengembangan</span></span>
            </div>
            <p className="text-xs text-slate-400 mt-4">
              © 2025 SuperBoost-AllerScan Aplikasi Deteksi Alergen Berbasis Data Mining & Machine Learning
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
