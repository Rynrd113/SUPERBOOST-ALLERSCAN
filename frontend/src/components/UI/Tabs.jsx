import React from 'react'
import Button from './Button'

const Tabs = ({ children, value, onValueChange, className = '' }) => {
  return (
    <div className={`w-full ${className}`}>
      {React.Children.map(children, child =>
        React.cloneElement(child, { value, onValueChange })
      )}
    </div>
  )
}

const TabsList = ({ children, value, onValueChange, className = '' }) => {
  return (
    <div className={`inline-flex h-10 items-center justify-center rounded-lg bg-gray-100 p-1 text-gray-500 ${className}`}>
      {React.Children.map(children, child =>
        React.cloneElement(child, { value, onValueChange })
      )}
    </div>
  )
}

const TabsTrigger = ({ children, value: currentValue, onValueChange, triggerValue, className = '' }) => {
  const isActive = currentValue === triggerValue
  
  return (
    <Button
      variant={isActive ? 'tabActive' : 'tab'}
      size="sm"
      className={`whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-white transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-allerscan-400 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${className}`}
      onClick={() => onValueChange(triggerValue)}
    >
      {children}
    </Button>
  )
}

const TabsContent = ({ children, value, contentValue, className = '' }) => {
  if (value !== contentValue) return null
  
  return (
    <div className={`mt-4 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-allerscan-400 focus-visible:ring-offset-2 ${className}`}>
      {children}
    </div>
  )
}

Tabs.List = TabsList
Tabs.Trigger = TabsTrigger
Tabs.Content = TabsContent

export default Tabs
