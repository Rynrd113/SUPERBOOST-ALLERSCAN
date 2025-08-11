# Database module for AllerScan
# SINGLE MySQL Database Implementation

from .allergen_database import database_manager, AllergenDatabaseManager

# Main database instance (MySQL only)
db = database_manager

__all__ = ['db', 'database_manager', 'AllergenDatabaseManager']
