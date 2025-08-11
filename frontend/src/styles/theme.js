// AllerScan Design System
export const theme = {
  colors: {
    // Primary Colors (Deep Blue - Dominant)
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6', // Main primary
      600: '#2563eb',
      700: '#1d4ed8', // Deep blue for headers
      800: '#1e40af',
      900: '#1e3a8a',
    },
    
    // Secondary Colors (Maroon - Institutional)
    secondary: {
      50: '#fdf2f8',
      100: '#fce7f3',
      200: '#fbcfe8',
      300: '#f9a8d4',
      400: '#f472b6',
      500: '#ec4899',
      600: '#db2777',
      700: '#be185d', // Maroon
      800: '#9d174d',
      900: '#831843',
    },
    
    // Accent Colors (Used sparingly)
    accent: {
      orange: '#f97316', // BIMA orange
      yellow: '#eab308', // DIKTISAINTEK yellow
      green: '#10b981',  // SUPERBOOST green
      pink: '#ec4899',   // SUPERBOOST pink
      lightBlue: '#06b6d4', // SUPERBOOST light blue
      gold: '#f59e0b',   // Universitas gold
    },
    
    // Neutral Colors
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    },
    
    // Status Colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
  },
  
  // Typography Scale
  typography: {
    fontFamily: {
      primary: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'Consolas', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',      // 12px
      sm: '0.875rem',     // 14px
      base: '1rem',       // 16px
      lg: '1.125rem',     // 18px
      xl: '1.25rem',      // 20px
      '2xl': '1.5rem',    // 24px
      '3xl': '1.875rem',  // 30px
      '4xl': '2.25rem',   // 36px
    },
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
  },
  
  // Spacing Scale (based on 4px grid)
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
  },
  
  // Border Radius
  borderRadius: {
    none: '0',
    sm: '0.25rem',    // 4px
    base: '0.375rem', // 6px
    md: '0.5rem',     // 8px
    lg: '0.75rem',    // 12px
    xl: '1rem',       // 16px
    '2xl': '1.5rem',  // 24px
    full: '50%',
  },
  
  // Shadows
  boxShadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  },
}

// Common Tailwind Classes
export const commonClasses = {
  // Layout
  container: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
  section: 'py-12 lg:py-16',
  
  // Cards
  card: 'bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200',
  cardHeader: 'px-6 py-4 border-b border-gray-100',
  cardBody: 'p-6',
  
  // Buttons
  btnPrimary: 'bg-primary-700 hover:bg-primary-800 text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200 shadow-sm hover:shadow-md',
  btnSecondary: 'bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-3 rounded-lg transition-colors duration-200',
  btnAccent: 'bg-accent-orange hover:bg-orange-600 text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200',
  
  // Form Elements
  input: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
  select: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200 bg-white',
  label: 'block text-sm font-medium text-gray-700 mb-2',
  
  // Typography
  heading1: 'text-4xl font-bold text-gray-900 mb-6',
  heading2: 'text-3xl font-bold text-gray-900 mb-4',
  heading3: 'text-2xl font-semibold text-gray-900 mb-3',
  heading4: 'text-xl font-semibold text-gray-800 mb-2',
  body: 'text-base text-gray-600 leading-relaxed',
  small: 'text-sm text-gray-500',
  
  // Tables
  table: 'min-w-full divide-y divide-gray-200',
  tableHeader: 'bg-gray-50 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
  tableCell: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900',
  
  // Navigation
  navItem: 'text-gray-600 hover:text-primary-700 font-medium transition-colors duration-200',
  navItemActive: 'text-primary-700 font-semibold border-b-2 border-primary-700',
  
  // Status
  statusSuccess: 'bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium',
  statusWarning: 'bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium',
  statusError: 'bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium',
}

export default theme;
