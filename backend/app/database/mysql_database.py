"""
🔄 MySQL Database - Compatibility Module

Modul ini menyediakan kompatibilitas untuk import yang mengharapkan mysql_database.py
Semua fungsionalitas sekarang terpusat dalam allergen_database.py

@author SuperBoost AllerScan Team  
@version 2.0.0
"""

# Import the main database manager for backward compatibility
from .allergen_database import database_manager as db, AllergenDatabaseManager

# Export the same interface
__all__ = ['db', 'AllergenDatabaseManager']
