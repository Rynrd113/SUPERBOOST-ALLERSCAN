#!/usr/bin/env python3
"""
Check latest database entries including form submissions
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager

def check_latest_entries():
    """Check latest 5 entries including form data"""
    try:
        print("🔍 CHECKING LATEST DATABASE ENTRIES...")
        
        db = database_manager
        
        # Get latest user_predictions (includes both Excel and form entries)
        results = db.get_dataset_with_results(limit=20)  # Get more records
        
        print(f"📊 Found {len(results)} records")
        
        if results:
            print(f"\n🔍 LATEST 5 RECORDS (sorting by created_at DESC):")
            # Sort by timestamp to see most recent first
            sorted_results = sorted(results, key=lambda x: x.get('created_at', ''), reverse=True)
            
            for i, record in enumerate(sorted_results[:5]):
                print(f"\nRecord {i+1}:")
                print(f"  Nama Produk: '{record.get('product_name', 'N/A')}'")
                print(f"  Bahan Utama: '{record.get('bahan_utama', 'N/A')}'")
                print(f"  Pemanis: '{record.get('pemanis', 'N/A')}'")
                print(f"  Lemak/Minyak: '{record.get('lemak_minyak', 'N/A')}'")
                print(f"  Penyedap Rasa: '{record.get('penyedap_rasa', 'N/A')}'")
                print(f"  Keterangan: '{record.get('keterangan', 'N/A')}'")
                print(f"  Created At: '{record.get('created_at', 'N/A')}'")
                
                # Identify form entries
                keterangan = record.get('keterangan', '')
                is_form_entry = 'form' in keterangan.lower()
                print(f"  Is Form Entry: {'Yes' if is_form_entry else 'No'}")
        
        # Also check form_test_results table
        print(f"\n🔍 CHECKING FORM_TEST_RESULTS TABLE:")
        form_results = db.get_form_results(limit=5)
        print(f"📊 Found {len(form_results)} form results")
        
        for i, record in enumerate(form_results[:3]):
            print(f"\nForm Record {i+1}:")
            print(f"  Nama Produk: '{record.get('product_name', 'N/A')}'")
            print(f"  Ingredients: '{record.get('ingredients', 'N/A')}'")
            print(f"  Alergen Detected: '{record.get('alergen_detected', 'N/A')}'")
            print(f"  Timestamp: '{record.get('test_timestamp', 'N/A')}'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_latest_entries()
