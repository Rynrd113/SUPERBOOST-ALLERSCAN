/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // AllerScan Brand Colors - Primary Blue Theme
        allerscan: {
          50: '#F0F9FF',   // Very light blue
          100: '#E0F2FE',  // Light blue
          200: '#BAE6FD',  // Light blue-200
          300: '#7DD3FC',  // Light blue-300
          400: '#38BDF8',  // Light blue-400
          500: '#0EA5E9',  // Primary blue (from logo) ⭐
          600: '#0284C7',  // Secondary blue (darker)
          700: '#0369A1',  // Deep blue
          800: '#075985',  // Very deep blue
          900: '#0C4A6E',  // Darkest blue
        },
        
        // Professional Color Palette
        primary: {
          50: '#FEF3C7',   // Amber light
          100: '#FDE68A',
          200: '#FCD34D',
          300: '#FBBF24', 
          400: '#F59E0B',  // Amber primary
          500: '#F59E0B',
          600: '#D97706',  // Amber dark
          700: '#B45309',
          800: '#92400E',
          900: '#78350F',
        },
        
        // Semantic Colors
        success: {
          50: '#ECFDF5',
          500: '#10B981',
          600: '#059669',
        },
        warning: {
          50: '#FFFBEB',
          500: '#F59E0B',
          600: '#D97706',
        },
        error: {
          50: '#FEF2F2',
          500: '#EF4444',
          600: '#DC2626',
        },
      },
      
      // Modern Shadows
      boxShadow: {
        'allerscan': '0 4px 14px 0 rgba(14, 165, 233, 0.15)',
        'allerscan-lg': '0 10px 25px -3px rgba(14, 165, 233, 0.1), 0 4px 6px -2px rgba(14, 165, 233, 0.05)',
      },
      
      // Animation for modern interactions
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}