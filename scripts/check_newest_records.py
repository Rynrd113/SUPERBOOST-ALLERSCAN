#!/usr/bin/env python3
"""
Check newest database records
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager

def check_newest_records():
    """Check newest database records"""
    try:
        print("🔍 CHECKING NEWEST DATABASE RECORDS...")
        
        db = database_manager
        
        # Get newest records (ORDER BY created_at DESC)
        with db.engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("""
                SELECT product_name, bahan_utama, pemanis, lemak_minyak, penyedap_rasa, 
                       keterangan, created_at
                FROM user_predictions 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            
            records = result.fetchall()
            
            print(f"📊 Found {len(records)} newest records")
            
            for i, record in enumerate(records, 1):
                print(f"\n📝 Record {i} (Newest):")
                print(f"  🏷️  Nama Produk: '{record[0]}'")
                print(f"  🥘 Bahan Utama: '{record[1]}'")
                print(f"  🍯 Pemanis: '{record[2]}'")
                print(f"  🛢️  Lemak/Minyak: '{record[3]}'")
                print(f"  🧂 Penyedap Rasa: '{record[4]}'")
                print(f"  📝 Keterangan: '{record[5]}'")
                print(f"  📅 Created: {record[6]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_newest_records()
