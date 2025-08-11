"""
🔄 MySQL Database - Compatibility Module

This file provides backward compatibility for imports that expect mysql_database.py
All functionality is now centralized in allergen_database.py

@author SuperBoost AllerScan Team  
@version 2.0.0
@updated 2025-08-11
"""

# Import the main database manager for backward compatibility
from .allergen_database import database_manager as db, AllergenDatabaseManager

# Export the same interface
__all__ = ['db', 'AllergenDatabaseManager']
