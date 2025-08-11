#!/usr/bin/env python3
"""
Simple debug script untuk memeriksa nilai database
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager

def check_database_values():
    """Check database values untuk kolom bermasalah"""
    try:
        print("🔍 CHECKING DATABASE VALUES...")
        
        db = database_manager
        results = db.get_dataset_with_results(limit=10)
        
        print(f"📊 Found {len(results)} records")
        
        if results:
            print("\n🔍 SAMPLE RECORDS:")
            for i, record in enumerate(results[:5]):
                print(f"\nRecord {i+1}:")
                print(f"  Nama Produk: '{record.get('product_name', 'N/A')}'")
                print(f"  Bahan Utama: '{record.get('bahan_utama', 'N/A')}'")
                print(f"  Pemanis: '{record.get('pemanis', 'N/A')}'")
                print(f"  Lemak/Minyak: '{record.get('lemak_minyak', 'N/A')}'")
                print(f"  Penyedap Rasa: '{record.get('penyedap_rasa', 'N/A')}'")
        
        # Check unique values
        print(f"\n📈 UNIQUE VALUES:")
        pemanis_values = [r.get('pemanis', '') for r in results]
        lemak_values = [r.get('lemak_minyak', '') for r in results]
        penyedap_values = [r.get('penyedap_rasa', '') for r in results]
        
        print(f"Pemanis unique: {set(pemanis_values)}")
        print(f"Lemak unique: {set(lemak_values)}")
        print(f"Penyedap unique: {set(penyedap_values)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_values()
