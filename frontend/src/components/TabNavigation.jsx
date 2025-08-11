import React from 'react'
import Button from './UI/Button'

const TabNavigation = ({ tabs, activeTab, onTabChange, className = '' }) => {
  return (
    <div className={`tab-navigation ${className}`}>
      {tabs.map((tab) => (
        <Button
          key={tab.id}
          variant={activeTab === tab.id ? 'primary' : 'secondary'}
          size="sm"
          onClick={() => onTabChange(tab.id)}
          className={`whitespace-nowrap ${activeTab === tab.id ? 'active' : ''}`}
        >
          {tab.icon && <tab.icon className="h-4 w-4 mr-2" />}
          {tab.label}
        </Button>
      ))}
    </div>
  )
}

export default TabNavigation
