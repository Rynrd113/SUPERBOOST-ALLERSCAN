#!/usr/bin/env python3
"""
Debug specific form entry to see exact values
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager
from sqlalchemy import text

def check_specific_form_entry():
    """Check the latest Roti entry specifically"""
    try:
        print("🔍 CHECKING LATEST ROTI ENTRY...")
        
        db = database_manager
        
        # Check user_predictions for Roti entry
        with db.engine.connect() as conn:
            # Look for latest Roti entry
            result = conn.execute(text("""
                SELECT product_name, bahan_utama, pemanis, lemak_minyak, penyedap_rasa, 
                       keterangan, alergen_predicted, confidence, hasil_deteksi, created_at
                FROM user_predictions 
                WHERE product_name LIKE '%Roti%'
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            
            print("📊 Dataset Results for 'Roti':")
            roti_entries = result.fetchall()
            
            if roti_entries:
                for i, row in enumerate(roti_entries):
                    print(f"\nEntry {i+1}:")
                    print(f"  Nama Produk: '{row[0]}'")
                    print(f"  Bahan Utama: '{row[1]}'")
                    print(f"  Pemanis: '{row[2]}'")
                    print(f"  Lemak/Minyak: '{row[3]}'")
                    print(f"  Penyedap Rasa: '{row[4]}'")
                    print(f"  Keterangan: '{row[5]}'")
                    print(f"  Confidence: {row[7]}")
                    print(f"  Created At: {row[9]}")
            else:
                print("❌ No Roti entries found in user_predictions")
            
            # Also check form_test_results
            form_result = conn.execute(text("""
                SELECT product_name, ingredients, alergen_detected, confidence, test_timestamp
                FROM form_test_results 
                WHERE product_name LIKE '%Roti%'
                ORDER BY test_timestamp DESC 
                LIMIT 3
            """))
            
            print(f"\n📋 Form Test Results for 'Roti':")
            form_entries = form_result.fetchall()
            
            for i, row in enumerate(form_entries):
                print(f"\nForm Entry {i+1}:")
                print(f"  Nama Produk: '{row[0]}'")
                print(f"  Ingredients: '{row[1]}'")
                print(f"  Alergen Detected: '{row[2]}'")
                print(f"  Confidence: {row[3]}")
                print(f"  Timestamp: {row[4]}")
                
                # Test parsing this ingredients string
                print(f"\n  🧪 Testing parsing of: '{row[1]}'")
                parsed = db._parse_ingredients_smart(row[1])
                print(f"    Bahan Utama: '{parsed['bahan_utama']}'")
                print(f"    Pemanis: '{parsed['pemanis']}'")  
                print(f"    Lemak/Minyak: '{parsed['lemak_minyak']}'")
                print(f"    Penyedap Rasa: '{parsed['penyedap_rasa']}'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_specific_form_entry()
