#!/usr/bin/env python3
"""
🚀 Setup MySQL Database for AllerScan
Creates database and tables if they don't exist
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def test_xampp_connection():
    """Test if XAMPP MySQL is running"""
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            charset='utf8mb4'
        )
        print("✅ XAMPP MySQL connection successful!")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ XAMPP MySQL connection failed: {e}")
        print("📋 Please make sure:")
        print("   1. XAMPP is running")
        print("   2. MySQL service is started in XAMPP")
        print("   3. Port 3306 is available")
        return False

def create_database():
    """Create AllerScan database"""
    try:
        # Load environment variables
        load_dotenv()
        
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = int(os.getenv('MYSQL_PORT', 3306))
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DATABASE', 'allerscan_db')
        
        # Connect without specifying database
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
        
        with engine.connect() as conn:
            # Create database
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
            print(f"✅ Database '{database}' created successfully!")
        
        # Now test connection with database
        db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            current_db = result.scalar()
            print(f"✅ Connected to database: {current_db}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create necessary tables"""
    try:
        # Import database class to trigger table creation
        from app.database.allergen_database import database_manager as db
        
        # Test connection
        if db.test_connection():
            print("✅ All tables created successfully!")
            return True
        else:
            print("❌ Failed to create tables")
            return False
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def show_database_info():
    """Show database information"""
    try:
        from app.database.allergen_database import database_manager as db
        
        with db.engine.connect() as conn:
            # Show tables
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            print("\n📊 Database Information:")
            print(f"   Database: allerscan_db")
            print(f"   Tables: {', '.join(tables)}")
            
            # Show table structures
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"   {table}: {count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up MySQL Database for AllerScan")
    print("=" * 50)
    
    # Step 1: Test XAMPP connection
    print("\n1️⃣ Testing XAMPP MySQL connection...")
    if not test_xampp_connection():
        return False
    
    # Step 2: Create database
    print("\n2️⃣ Creating database...")
    if not create_database():
        return False
    
    # Step 3: Create tables
    print("\n3️⃣ Creating tables...")
    if not create_tables():
        return False
    
    # Step 4: Show database info
    print("\n4️⃣ Database setup complete!")
    show_database_info()
    
    print("\n✅ MySQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Restart the backend server")
    print("   2. Use 'Load Dataset & Generate Predictions' in frontend")
    print("   3. Test form submissions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
