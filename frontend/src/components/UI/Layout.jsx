import React from 'react'

const Container = ({ children, size = 'default', className = '' }) => {
  const sizes = {
    sm: 'max-w-4xl',
    default: 'max-w-6xl',
    lg: 'max-w-7xl',
    full: 'max-w-full'
  }
  
  return (
    <div className={`mx-auto px-4 sm:px-6 lg:px-8 ${sizes[size]} ${className}`}>
      {children}
    </div>
  )
}

const Section = ({ children, className = '', spacing = 'default' }) => {
  const spacings = {
    sm: 'py-8',
    default: 'py-12',
    lg: 'py-16',
    xl: 'py-20'
  }
  
  return (
    <section className={`${spacings[spacing]} ${className}`}>
      {children}
    </section>
  )
}

const Grid = ({ children, cols = 1, gap = 'default', className = '' }) => {
  const colsClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  }
  
  const gaps = {
    sm: 'gap-4',
    default: 'gap-6',
    lg: 'gap-8'
  }
  
  return (
    <div className={`grid ${colsClasses[cols]} ${gaps[gap]} ${className}`}>
      {children}
    </div>
  )
}

const Flex = ({ children, direction = 'row', align = 'start', justify = 'start', wrap = false, gap = 'default', className = '' }) => {
  const directions = {
    row: 'flex-row',
    col: 'flex-col'
  }
  
  const aligns = {
    start: 'items-start',
    center: 'items-center',
    end: 'items-end',
    stretch: 'items-stretch'
  }
  
  const justifies = {
    start: 'justify-start',
    center: 'justify-center',
    end: 'justify-end',
    between: 'justify-between',
    around: 'justify-around'
  }
  
  const gaps = {
    sm: 'gap-2',
    default: 'gap-4',
    lg: 'gap-6'
  }
  
  const wrapClass = wrap ? 'flex-wrap' : ''
  
  return (
    <div className={`flex ${directions[direction]} ${aligns[align]} ${justifies[justify]} ${gaps[gap]} ${wrapClass} ${className}`}>
      {children}
    </div>
  )
}

export { Container, Section, Grid, Flex }
