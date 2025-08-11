#!/usr/bin/env python3
"""
Check table structure
"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

from app.database.allergen_database import database_manager
from sqlalchemy import text

def check_table_structure():
    try:
        with database_manager.engine.connect() as conn:
            result = conn.execute(text('DESCRIBE user_predictions'))
            print('📊 user_predictions table structure:')
            for row in result:
                print(f'  {row[0]} - {row[1]}')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_table_structure()
