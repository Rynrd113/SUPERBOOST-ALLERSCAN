#!/usr/bin/env python3
"""
Debug script untuk memeriksa nilai sebenarnya di database
untuk kolom Pemanis, Lemak/Minyak, dan Penyedap Rasa
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.database.allergen_database import database_manager
import pandas as pd

def debug_database_values():
    """Debug nilai database untuk mencari masalah 'tidak ada'"""
    
    print("🔍 DEBUGGING DATABASE VALUES")
    print("=" * 60)
    
    try:
        # Get database instance
        db = database_manager
        
        # Get raw dataset results
        results = db.get_prediction_history(limit=10)
        
        if not results or not results.get('records'):
            print("❌ No data found in database")
            return
        
        records = results['records']
        print(f"📊 Found {len(records)} records")
        print("\n🔍 Sample data from database:")
        
        for i, record in enumerate(records[:5]):  # First 5 records
            print(f"\n--- Record {i+1} ---")
            print(f"Nama Produk: {record.get('product_name', 'N/A')}")
            print(f"Bahan Utama: {record.get('bahan_utama', 'N/A')}")
            print(f"Pemanis: '{record.get('pemanis', 'N/A')}'")
            print(f"Lemak/Minyak: '{record.get('lemak_minyak', 'N/A')}'")
            print(f"Penyedap Rasa: '{record.get('penyedap_rasa', 'N/A')}'")
            print(f"Alergen Actual: {record.get('alergen_actual', 'N/A')}")
        
        # Count unique values for problematic columns
        print("\n📈 UNIQUE VALUES ANALYSIS:")
        
        # Extract values
        pemanis_values = [record.get('pemanis', '') for record in records]
        lemak_values = [record.get('lemak_minyak', '') for record in records]  
        penyedap_values = [record.get('penyedap_rasa', '') for record in records]
        
        print(f"\nPemanis unique values: {set(pemanis_values)}")
        print(f"Lemak/Minyak unique values: {set(lemak_values)}")
        print(f"Penyedap Rasa unique values: {set(penyedap_values)}")
        
        # Count empty/null values
        empty_pemanis = sum(1 for v in pemanis_values if not v or v.strip() == '')
        empty_lemak = sum(1 for v in lemak_values if not v or v.strip() == '')
        empty_penyedap = sum(1 for v in penyedap_values if not v or v.strip() == '')
        
        print(f"\n📊 EMPTY VALUES COUNT:")
        print(f"Empty Pemanis: {empty_pemanis}/{len(records)}")
        print(f"Empty Lemak/Minyak: {empty_lemak}/{len(records)}")
        print(f"Empty Penyedap Rasa: {empty_penyedap}/{len(records)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔍 COMPARING WITH ORIGINAL EXCEL DATA:")
    try:
        # Load original Excel
        df = pd.read_excel('data/raw/Dataset Bahan Makanan & Alergen.xlsx', sheet_name='Dataset')
        print(f"Excel records: {len(df)}")
        print(f"Excel Pemanis unique values: {len(df['Pemanis'].unique())} values")
        print(f"Excel sample Pemanis: {list(df['Pemanis'].head())}")
        print(f"Excel sample Lemak/Minyak: {list(df['Lemak/Minyak'].head())}")
        print(f"Excel sample Penyedap Rasa: {list(df['Penyedap Rasa'].head())}")
        
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")

if __name__ == "__main__":
    debug_database_values()
