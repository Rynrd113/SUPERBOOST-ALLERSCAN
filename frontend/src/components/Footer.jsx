import { Heart, Shield, ExternalLink, Mail, Phone, MapPin } from 'lucide-react'
import LogoSection from './UI/LogoSection'

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-slate-900 to-slate-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-3 bg-blue-600 rounded-2xl shadow-xl">
                <img 
                  src="/logo/Logo SuperBoost-AllerScan.png"
                  alt="SuperBoost AllerScan Logo"
                  className="h-8 w-8 object-contain"
                />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">SuperBoost AllerScan</h3>
                <p className="text-blue-200 text-sm">AI-Powered Allergen Detection</p>
              </div>
            </div>
            <p className="text-slate-300 text-sm leading-relaxed max-w-md mb-6">
              Sistem deteksi alergen makanan berbasis AI menggunakan algoritma SVM + AdaBoost 
              dengan akurasi 93.7% untuk menjaga keamanan dan kesehatan konsumen.
            </p>
            
            {/* Logos Section - Using LogoSection Component */}
            <div className="space-y-3">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Supported By</p>
              <LogoSection variant="footer" className="!space-x-4" showAllLogos={true} />
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Sumber Daya</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors duration-200 text-sm flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Dokumentasi API
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors duration-200 text-sm flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Daftar Alergen
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors duration-200 text-sm flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Panduan Penggunaan
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors duration-200 text-sm flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Research Paper
                </a>
              </li>
            </ul>
          </div>
          
          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Kontak</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start space-x-2 text-slate-300">
                <Mail className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium">Email:</p>
                  <a href="mailto:allerscan@kartur.ac.id" className="hover:text-white transition-colors">
                    allerscan@kartur.ac.id
                  </a>
                </div>
              </li>
              <li className="flex items-start space-x-2 text-slate-300">
                <Phone className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium">Telepon:</p>
                  <span>+62 (0)21-ALLERSCAN</span>
                </div>
              </li>
              <li className="flex items-start space-x-2 text-slate-300">
                <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium">Alamat:</p>
                  <span className="text-xs leading-relaxed">
                    Universitas Nasional Karangturi<br />
                    Semarang, Jawa Tengah
                  </span>
                </div>
              </li>
            </ul>
          </div>
        </div>
        
        {/* Bottom Footer */}
        <div className="border-t border-slate-700 pt-8">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-2 text-slate-400 text-sm">
              <Heart className="h-4 w-4 text-red-500" />
              <span>Made with love for food safety awareness</span>
            </div>
            <div className="text-slate-400 text-sm text-center md:text-right">
              <p>© 2025 SuperBoost AllerScan Project</p>
              <p className="text-xs mt-1">
                Program Hibah Penelitian Kemendikbudristek 2025
              </p>
            </div>
          </div>
        </div>
        
      </div>
    </footer>
  )
}

export default Footer
