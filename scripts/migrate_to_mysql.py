#!/usr/bin/env python3
"""
🔄 Migrate data from SQLite to MySQL for AllerScan
Transfers existing data if SQLite database exists
"""

import os
import sys
import sqlite3
from pathlib import Path

# Add parent directory to path to import app modules
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from app.database.allergen_database import database_manager as db
from dotenv import load_dotenv
from sqlalchemy import text

def check_sqlite_exists():
    """Check if SQLite database exists"""
    sqlite_path = Path("allergen_results.db")
    if sqlite_path.exists():
        print(f"✅ Found SQLite database: {sqlite_path}")
        return str(sqlite_path)
    else:
        print("ℹ️ No SQLite database found - starting fresh with MySQL")
        return None

def migrate_data(sqlite_path):
    """Migrate data from SQLite to MySQL"""
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Check tables in SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in sqlite_cursor.fetchall()]
        print(f"📊 Found tables in SQLite: {tables}")
        
        migrated_count = 0
        
        # Migrate dataset_results if exists
        if 'dataset_results' in tables:
            sqlite_cursor.execute("SELECT COUNT(*) FROM dataset_results")
            count = sqlite_cursor.fetchone()[0]
            print(f"📋 Found {count} records in dataset_results")
            
            if count > 0:
                # Get all records
                sqlite_cursor.execute("""
                    SELECT nama_produk, bahan_utama, pemanis, lemak_minyak, 
                           penyedap_rasa, keterangan, alergen_actual, 
                           alergen_predicted, confidence, hasil_deteksi
                    FROM dataset_results
                """)
                
                records = sqlite_cursor.fetchall()
                
                # Insert into MySQL
                with db.engine.connect() as mysql_conn:
                    for record in records:
                        mysql_conn.execute(text("""
                            INSERT INTO dataset_results 
                            (nama_produk, bahan_utama, pemanis, lemak_minyak, 
                             penyedap_rasa, keterangan, alergen_actual, 
                             alergen_predicted, confidence, hasil_deteksi)
                            VALUES (:nama_produk, :bahan_utama, :pemanis, :lemak_minyak,
                                    :penyedap_rasa, :keterangan, :alergen_actual,
                                    :alergen_predicted, :confidence, :hasil_deteksi)
                        """), {
                            'nama_produk': record[0],
                            'bahan_utama': record[1],
                            'pemanis': record[2],
                            'lemak_minyak': record[3],
                            'penyedap_rasa': record[4],
                            'keterangan': record[5],
                            'alergen_actual': record[6],
                            'alergen_predicted': record[7],
                            'confidence': record[8],
                            'hasil_deteksi': record[9]
                        })
                    mysql_conn.commit()
                
                migrated_count += count
                print(f"✅ Migrated {count} dataset records")
        
        # Migrate form_test_results if exists
        if 'form_test_results' in tables:
            sqlite_cursor.execute("SELECT COUNT(*) FROM form_test_results")
            count = sqlite_cursor.fetchone()[0]
            print(f"📋 Found {count} records in form_test_results")
            
            if count > 0:
                # Get all records
                sqlite_cursor.execute("""
                    SELECT nama_produk, ingredients, alergen_detected, 
                           confidence, detailed_results, total_allergens,
                           ip_address, user_agent
                    FROM form_test_results
                """)
                
                records = sqlite_cursor.fetchall()
                
                # Insert into MySQL
                with db.engine.connect() as mysql_conn:
                    for record in records:
                        mysql_conn.execute(text("""
                            INSERT INTO form_test_results 
                            (nama_produk, ingredients, alergen_detected, confidence,
                             detailed_results, total_allergens, ip_address, user_agent)
                            VALUES (:nama_produk, :ingredients, :alergen_detected, :confidence,
                                    :detailed_results, :total_allergens, :ip_address, :user_agent)
                        """), {
                            'nama_produk': record[0],
                            'ingredients': record[1],
                            'alergen_detected': record[2],
                            'confidence': record[3],
                            'detailed_results': record[4],
                            'total_allergens': record[5],
                            'ip_address': record[6],
                            'user_agent': record[7]
                        })
                    mysql_conn.commit()
                
                migrated_count += count
                print(f"✅ Migrated {count} form test records")
        
        sqlite_conn.close()
        
        print(f"\n✅ Migration completed! Total records migrated: {migrated_count}")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

def verify_migration():
    """Verify migrated data in MySQL"""
    try:
        stats = db.get_statistics()
        print(f"\n📊 MySQL Database Status:")
        print(f"   Dataset records: {stats['dataset_records']}")
        print(f"   Form test records: {stats['form_test_records']}")
        print(f"   Average confidence: {stats['average_confidence']}")
        print(f"   Detected items: {stats['detected_count']}")
        print(f"   Not detected items: {stats['not_detected_count']}")
        return True
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    print("🔄 AllerScan Database Migration: SQLite → MySQL")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check if SQLite exists
    sqlite_path = check_sqlite_exists()
    
    if sqlite_path:
        print(f"\n🚀 Starting migration from {sqlite_path} to MySQL...")
        
        # Import required modules for migration
        from sqlalchemy import text
        
        # Migrate data
        if migrate_data(sqlite_path):
            print("✅ Data migration successful!")
        else:
            print("❌ Data migration failed!")
            return False
    else:
        print("\n✅ No migration needed - starting fresh with MySQL")
    
    # Verify final state
    print("\n🔍 Verifying MySQL database...")
    verify_migration()
    
    print("\n🎉 Migration process completed!")
    print("\n📋 Next steps:")
    print("   1. Backend is now using MySQL")
    print("   2. Test the application in the browser")
    print("   3. Use 'Load Dataset' to populate with fresh data if needed")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
