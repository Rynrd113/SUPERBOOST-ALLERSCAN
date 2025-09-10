#!/usr/bin/env python3
"""
Script untuk menganalisis kolom alergen dan memperbaiki prediksi alergen spesifik
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import pandas as pd
from collections import Counter

def analyze_allergen_column():
    print("=" * 60)
    print("Analisis Kolom Alergen untuk Perbaikan Prediksi")
    print("=" * 60)
    
    try:
        dataset_path = "data/raw/Dataset Bahan Makanan & Alergen.xlsx"
        df = pd.read_excel(dataset_path)
        
        print(f"\n1. ANALISIS KOLOM ALERGEN:")
        print(f"   Jumlah data: {len(df)}")
        print(f"   Kolom alergen: {df['Alergen'].head(10).tolist()}")
        
        # Hitung distribusi alergen
        print(f"\n2. DISTRIBUSI ALERGEN:")
        all_allergens = []
        for alergen_str in df['Alergen'].dropna():
            if isinstance(alergen_str, str):
                # Split alergen yang dipisah koma
                allergens = [a.strip() for a in alergen_str.split(',')]
                all_allergens.extend(allergens)
        
        allergen_counts = Counter(all_allergens)
        print(f"   Total unique alergen: {len(allergen_counts)}")
        print(f"   Alergen paling umum:")
        for allergen, count in allergen_counts.most_common(15):
            print(f"      {allergen}: {count} kali")
        
        # Analisis pattern
        print(f"\n3. ANALISIS PATTERN:")
        prediksi_counts = df['Prediksi'].value_counts()
        print(f"   Distribusi prediksi:")
        for pred, count in prediksi_counts.items():
            print(f"      {pred}: {count}")
        
        # Sample data untuk analisa pattern
        print(f"\n4. SAMPLE DATA ALERGEN:")
        alergen_samples = df[['Bahan Utama', 'Alergen', 'Prediksi']].head(10)
        print(alergen_samples.to_string())
        
        # Analisis bahan utama yang sering menyebabkan alergen
        print(f"\n5. BAHAN UTAMA VS ALERGEN:")
        bahan_alergen = df[df['Prediksi'] == 'Mengandung Alergen']['Bahan Utama'].value_counts().head(10)
        print(f"   Bahan utama paling sering mengandung alergen:")
        for bahan, count in bahan_alergen.items():
            related_allergens = df[df['Bahan Utama'] == bahan]['Alergen'].value_counts().head(3)
            print(f"      {bahan}: {count} kali")
            for alergen, freq in related_allergens.items():
                print(f"        -> {alergen}: {freq}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    analyze_allergen_column()
