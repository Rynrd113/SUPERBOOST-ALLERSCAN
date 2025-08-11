/**
 * LogoSection Component - Reusable Logo Display
 * 
 * Eliminasi duplikasi logo di berbagai halaman
 * Konsisten dengan DRY principles
 */

import React from 'react'

const LogoSection = ({ 
  variant = 'full', // 'full', 'compact', 'footer'
  className = '',
  showAllLogos = true 
}) => {
  const sizeClasses = {
    full: 'h-16', // Logo size untuk header utama
    compact: 'h-14', // Logo size untuk mobile/compact view
    footer: 'h-10' // Logo size untuk footer
  }

  const logos = [
    {
      src: "/logo/Logo SuperBoost-AllerScan.png",
      alt: "SuperBoost AllerScan - Sistem Deteksi Alergen Makanan",
      priority: 1,
      isMainLogo: true, // Flag untuk logo utama
      // Sama besar dengan logo lain - menghilangkan customSize
    },
    {
      src: "/logo/Logo Unkartur.png", 
      alt: "Universitas Nasional Karangturi (Unkartur) Logo",
      priority: 2
    },
    {
      src: "/logo/Logo Bima-Dikti.png",
      alt: "Bima Dikti Kemendikbudristek Logo", 
      priority: 3,
      showOnlyIfAll: true
    },
    {
      src: "/logo/Logo Diktisaintek Berdampak.png",
      alt: "Diktisaintek Berdampak Logo",
      priority: 4,
      showOnlyIfAll: true
    }
  ]

  const visibleLogos = showAllLogos 
    ? logos 
    : logos.filter(logo => !logo.showOnlyIfAll)

  return (
    <div className={`flex items-center justify-center space-x-8 ${className}`}>
      {visibleLogos.map((logo, index) => {
        // Semua logo menggunakan ukuran yang sama
        const logoSize = sizeClasses[variant]
        
        return (
          <div
            key={index}
            className={`flex items-center justify-center ${
              logo.isMainLogo ? 'bg-white/10 rounded-lg p-3 border-2 border-white/20' : ''
            }`}
          >
            <img
              src={logo.src}
              alt={logo.alt}
              className={`object-contain ${logoSize} max-w-full`}
              loading={logo.priority <= 2 ? 'eager' : 'lazy'}
            />
          </div>
        )
      })}
    </div>
  )
}

export default LogoSection
