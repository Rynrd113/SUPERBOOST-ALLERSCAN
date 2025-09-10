#!/usr/bin/env python3
"""
Script untuk melihat format data training dan menguji dengan data yang sesuai
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import pandas as pd
from backend.app.models.inference.predictor import predictor

def analyze_dataset():
    print("=" * 60)
    print("Analisis Dataset Training")
    print("=" * 60)
    
    # Load dataset untuk melihat format data
    try:
        dataset_path = "data/raw/Dataset Bahan Makanan & Alergen.xlsx"
        df = pd.read_excel(dataset_path)
        
        print(f"\n1. DATASET INFO:")
        print(f"   Shape: {df.shape}")
        print(f"   Kolom: {list(df.columns)}")
        
        print(f"\n2. SAMPLE DATA (5 baris pertama):")
        print(df.head().to_string())
        
        print(f"\n3. UNIQUE VALUES PER KOLOM:")
        for col in df.columns:
            if col in ['Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa']:
                unique_vals = df[col].dropna().unique()
                print(f"   {col}: {len(unique_vals)} nilai unik")
                print(f"      Contoh: {list(unique_vals[:10])}")
        
        # Test dengan data yang sesuai dengan training data
        print(f"\n4. TEST DENGAN DATA TRAINING:")
        
        # Ambil contoh dari data training
        sample_row = df.iloc[0]
        test_input = {
            'bahan_utama': sample_row['Bahan Utama'],
            'pemanis': sample_row['Pemanis'], 
            'lemak_minyak': sample_row['Lemak/Minyak'],
            'penyedap_rasa': sample_row['Penyedap Rasa']
        }
        
        print(f"   Input dari data training: {test_input}")
        print(f"   Expected alergen: {sample_row.get('Alergen', 'N/A')}")
        
        # Test prediksi
        result = predictor.predict(test_input)
        print(f"   Hasil prediksi: {result}")
        
        # Test dengan kacang tanah (biasanya alergen)
        print(f"\n5. TEST DENGAN DATA KACANG TANAH:")
        peanut_rows = df[df['Bahan Utama'].str.contains('kacang', case=False, na=False)]
        if len(peanut_rows) > 0:
            peanut_sample = peanut_rows.iloc[0]
            peanut_input = {
                'bahan_utama': peanut_sample['Bahan Utama'],
                'pemanis': peanut_sample['Pemanis'], 
                'lemak_minyak': peanut_sample['Lemak/Minyak'],
                'penyedap_rasa': peanut_sample['Penyedap Rasa']
            }
            print(f"   Input kacang: {peanut_input}")
            print(f"   Expected alergen: {peanut_sample.get('Alergen', 'N/A')}")
            
            result = predictor.predict(peanut_input)
            print(f"   Hasil prediksi: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    analyze_dataset()
