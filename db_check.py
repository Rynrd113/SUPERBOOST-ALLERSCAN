#!/usr/bin/env python3
"""
🔍 Quick Database Check untuk memverifikasi setup di TablePlus
Cek koneksi dan isi tabel database allerscan_db
"""

import pymysql
import json
from datetime import datetime

# Database configuration untuk DBngin
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'allerscan_db'
}

def check_database_connection():
    """Check database connection"""
    print("🔧 Checking database connection...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() as version")
            result = cursor.fetchone()
            print(f"✅ MySQL Version: {result['version']}")
            
            cursor.execute("SELECT DATABASE() as current_db")
            result = cursor.fetchone()
            print(f"✅ Current Database: {result['current_db']}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_tables():
    """Check existing tables"""
    print("\n🔧 Checking tables...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"   - {table_name}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"     Rows: {count}")
                
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def insert_test_data():
    """Insert test prediction data"""
    print("\n🔧 Inserting test data...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        
        test_data = {
            'input_text': 'tepung terigu, telur, susu, mentega',
            'predicted_allergens': json.dumps(['gluten', 'telur', 'susu']),
            'confidence_scores': json.dumps({'gluten': 0.95, 'telur': 0.88, 'susu': 0.92}),
            'processing_time_ms': 150.5,
            'model_version': 'SVM+AdaBoost v1.0'
        }
        
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO allergen_results 
            (input_text, predicted_allergens, confidence_scores, processing_time_ms, model_version)
            VALUES (%(input_text)s, %(predicted_allergens)s, %(confidence_scores)s, 
                   %(processing_time_ms)s, %(model_version)s)
            """
            
            cursor.execute(insert_query, test_data)
            connection.commit()
            
            print("✅ Test data inserted successfully!")
            print(f"   Input: {test_data['input_text']}")
            print(f"   Allergens: {test_data['predicted_allergens']}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error inserting test data: {e}")
        return False

def view_recent_data():
    """View recent prediction data"""
    print("\n🔧 Viewing recent data...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, input_text, predicted_allergens, confidence_scores, 
                       prediction_timestamp, processing_time_ms, model_version
                FROM allergen_results 
                ORDER BY prediction_timestamp DESC 
                LIMIT 5
            """)
            
            results = cursor.fetchall()
            
            if results:
                print(f"📊 Found {len(results)} recent predictions:")
                for row in results:
                    print(f"\n   ID: {row['id']}")
                    print(f"   Input: {row['input_text'][:50]}...")
                    print(f"   Allergens: {row['predicted_allergens']}")
                    print(f"   Timestamp: {row['prediction_timestamp']}")
                    print(f"   Processing: {row['processing_time_ms']}ms")
            else:
                print("📊 No prediction data found yet")
                
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error viewing data: {e}")
        return False

def generate_tableplus_info():
    """Generate connection info for TablePlus"""
    print("\n📋 TablePlus Connection Info:")
    print("=" * 40)
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Port: {DB_CONFIG['port']}")
    print(f"Username: {DB_CONFIG['user']}")
    print(f"Password: {DB_CONFIG['password'] or '(empty)'}")
    print(f"Database: {DB_CONFIG['database']}")
    print("=" * 40)
    print("\n💡 Untuk connect ke TablePlus:")
    print("1. Buka TablePlus")
    print("2. Klik 'Create a new connection'")
    print("3. Pilih MySQL")
    print("4. Masukkan info di atas")
    print("5. Test connection dan save")

def main():
    """Main function"""
    print("🚀 AllerScan Database Quick Check dengan DBngin")
    print("=" * 50)
    
    if not check_database_connection():
        return
        
    if not check_tables():
        return
        
    insert_test_data()
    view_recent_data()
    generate_tableplus_info()
    
    print("\n🎉 Database check completed!")
    print("💡 Anda sekarang bisa connect ke database menggunakan TablePlus")

if __name__ == "__main__":
    main()
