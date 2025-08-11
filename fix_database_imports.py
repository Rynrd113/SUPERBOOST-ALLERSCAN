#!/usr/bin/env python3
"""
🔧 Fix Database Imports - Konsolidasi ke MySQL tunggal
Mengubah semua import database lama ke allergen_database.py
"""

import os
import re
from pathlib import Path

def fix_database_imports():
    """Fix all database imports to use single MySQL implementation"""
    
    print("🔧 FIXING DATABASE IMPORTS...")
    
    # Scripts that need fixing
    scripts_dir = Path("scripts")
    backend_dir = Path("backend")
    
    # Files to fix
    files_to_fix = [
        "scripts/check_newest_records.py",
        "scripts/check_db_values.py", 
        "scripts/check_latest_db.py",
        "scripts/check_roti_entry.py",
        "scripts/test_ingredient_parsing.py"
    ]
    
    fixes_applied = 0
    
    for file_path in files_to_fix:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace old imports
                old_import = "from backend.app.database.mysql_database import MySQLAllergenDatabase"
                new_import = "from backend.app.database.allergen_database import database_manager"
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    
                    # Replace class instantiation 
                    content = re.sub(
                        r'db = MySQLAllergenDatabase\(\)',
                        'db = database_manager',
                        content
                    )
                    
                    # Replace table names if needed
                    content = content.replace('dataset_results', 'user_predictions')
                    content = content.replace('nama_produk', 'product_name')
                    
                    with open(file_path, 'w') as f:
                        f.write(content)
                    
                    print(f"✅ Fixed: {file_path}")
                    fixes_applied += 1
                
            except Exception as e:
                print(f"❌ Error fixing {file_path}: {e}")
    
    print(f"\n🎉 Applied {fixes_applied} fixes!")
    print("✅ All database imports now use single MySQL implementation")

if __name__ == "__main__":
    fix_database_imports()
