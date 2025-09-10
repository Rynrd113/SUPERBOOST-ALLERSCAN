#!/usr/bin/env python3
"""
🛠️ Database Setup Script untuk AllerScan di Mac dengan DBngin
Setup database dan tabel yang diperlukan untuk project AllerScan
"""

import os
import sys
import pymysql
from pathlib import Path

# Database configuration untuk DBngin
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # DBngin biasanya tidak pakai password untuk development
    'database': 'allerscan_db'
}

def create_database():
    """Create database allerscan_db if not exists"""
    print("🔧 Creating database if not exists...")
    
    try:
        # Connect tanpa database specific
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    finally:
        connection.close()
    
    return True

def create_tables():
    """Create necessary tables"""
    print("🔧 Creating tables...")
    
    try:
        # Connect to specific database
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Allergen results table
            create_allergen_results = """
            CREATE TABLE IF NOT EXISTS allergen_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_text TEXT NOT NULL,
                predicted_allergens JSON,
                confidence_scores JSON,
                prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                processing_time_ms FLOAT,
                model_version VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            
            cursor.execute(create_allergen_results)
            print("✅ Table 'allergen_results' created successfully!")
            
            # Training data table (for dataset)
            create_training_data = """
            CREATE TABLE IF NOT EXISTS training_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bahan_makanan TEXT NOT NULL,
                alergen VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            
            cursor.execute(create_training_data)
            print("✅ Table 'training_data' created successfully!")
            
        connection.commit()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        connection.close()
    
    return True

def test_connection():
    """Test database connection"""
    print("🔧 Testing database connection...")
    
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        try:
            connection.close()
        except:
            pass

def main():
    """Main setup function"""
    print("🚀 Starting AllerScan Database Setup untuk DBngin...")
    print(f"📊 Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    # Check if we can connect to MySQL
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        connection.close()
        print("✅ MySQL connection successful!")
    except Exception as e:
        print(f"❌ Cannot connect to MySQL: {e}")
        print("💡 Pastikan DBngin sudah running dan MySQL service aktif")
        return False
    
    # Setup database
    if not create_database():
        return False
    
    if not create_tables():
        return False
        
    if not test_connection():
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("📋 Summary:")
    print(f"   - Database: {DB_CONFIG['database']}")
    print(f"   - Tables: allergen_results, training_data")
    print("   - Ready for development!")
    
    return True

if __name__ == "__main__":
    main()
