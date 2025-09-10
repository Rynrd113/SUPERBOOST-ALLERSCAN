"""
Implementasi perbaikan untuk predictor.py - menambahkan deteksi alergen spesifik
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import re

def create_allergen_mapping():
    """
    Membuat mapping dari bahan ke alergen berdasarkan data training
    """
    print("=" * 60)
    print("Membuat Mapping Bahan ke Alergen")
    print("=" * 60)
    
    # Load dataset
    dataset_path = "data/raw/Dataset Bahan Makanan & Alergen.xlsx"
    df = pd.read_excel(dataset_path)
    
    # Buat mapping bahan ke alergen
    ingredient_to_allergen = defaultdict(set)
    
    for idx, row in df.iterrows():
        ingredients = [
            str(row['Bahan Utama']).lower().strip(),
            str(row['Pemanis']).lower().strip(), 
            str(row['Lemak/Minyak']).lower().strip(),
            str(row['Penyedap Rasa']).lower().strip()
        ]
        
        # Parse alergen
        alergen_str = str(row['Alergen'])
        if alergen_str != 'nan' and alergen_str != 'Tidak Ada':
            allergens = [a.strip() for a in alergen_str.split(',')]
            
            # Map setiap ingredient ke alergen
            for ingredient in ingredients:
                if ingredient != 'nan' and ingredient != 'tidak ada':
                    for allergen in allergens:
                        ingredient_to_allergen[ingredient].add(allergen)
    
    print(f"Total ingredient mappings: {len(ingredient_to_allergen)}")
    
    # Tampilkan beberapa contoh mapping
    print(f"\nContoh mapping:")
    for ingredient, allergens in list(ingredient_to_allergen.items())[:10]:
        print(f"   {ingredient} -> {list(allergens)}")
    
    # Buat rule-based detector
    print(f"\n" + "="*40)
    print("RULE-BASED ALLERGEN DETECTOR")
    print("="*40)
    
    def detect_allergens_rule_based(input_data):
        """
        Deteksi alergen berdasarkan rule dan mapping
        """
        detected_allergens = set()
        confidence_scores = {}
        
        # Mapping khusus untuk deteksi alergen umum
        allergen_keywords = {
            'Kacang': ['kacang', 'almond', 'pinus', 'nut'],
            'Produk Susu': ['susu', 'keju', 'mentega', 'butter', 'cream', 'dairy', 'yogurt'],
            'Gandum': ['tepung', 'wheat', 'flour', 'roti', 'bread', 'pasta', 'mie'],
            'Telur': ['telur', 'egg'],
            'Ikan': ['ikan', 'salmon', 'tuna', 'fish', 'teri'],
            'Kerang-Kerangan': ['udang', 'kerang', 'lobster', 'crab', 'shrimp'],
            'Kedelai': ['kedelai', 'soy', 'tofu', 'tempe'],
            'Seledri': ['seledri', 'celery']
        }
        
        # Gabungkan semua input menjadi text
        all_ingredients = ' '.join([
            str(input_data.get('bahan_utama', '')),
            str(input_data.get('pemanis', '')),
            str(input_data.get('lemak_minyak', '')),
            str(input_data.get('penyedap_rasa', ''))
        ]).lower()
        
        # Deteksi berdasarkan keyword
        for allergen, keywords in allergen_keywords.items():
            for keyword in keywords:
                if keyword in all_ingredients:
                    detected_allergens.add(allergen)
                    # Berikan confidence berdasarkan exact match
                    if keyword == input_data.get('bahan_utama', '').lower():
                        confidence_scores[allergen] = 0.9  # High confidence untuk bahan utama
                    else:
                        confidence_scores[allergen] = 0.7  # Medium confidence untuk ingredient lain
        
        # Mapping berdasarkan data training
        for field in ['bahan_utama', 'pemanis', 'lemak_minyak', 'penyedap_rasa']:
            ingredient = str(input_data.get(field, '')).lower().strip()
            if ingredient in ingredient_to_allergen:
                for allergen in ingredient_to_allergen[ingredient]:
                    detected_allergens.add(allergen)
                    confidence_scores[allergen] = confidence_scores.get(allergen, 0.8)
        
        return detected_allergens, confidence_scores
    
    # Test dengan beberapa contoh
    test_cases = [
        {
            'bahan_utama': 'Kacang Almond',
            'pemanis': 'Gula Pasir', 
            'lemak_minyak': 'Mentega',
            'penyedap_rasa': 'Tepung'
        },
        {
            'bahan_utama': 'kacang tanah',
            'pemanis': 'gula',
            'lemak_minyak': 'minyak',
            'penyedap_rasa': 'garam'
        },
        {
            'bahan_utama': 'susu',
            'pemanis': 'tidak ada',
            'lemak_minyak': 'mentega', 
            'penyedap_rasa': 'vanilla'
        },
        {
            'bahan_utama': 'udang',
            'pemanis': 'tidak ada',
            'lemak_minyak': 'minyak',
            'penyedap_rasa': 'garam'
        }
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_input}")
        allergens, confidences = detect_allergens_rule_based(test_input)
        
        if allergens:
            print(f"   Detected allergens:")
            for allergen in allergens:
                confidence = confidences.get(allergen, 0.5)
                print(f"      {allergen}: {confidence:.2f}")
        else:
            print(f"   No allergens detected")
    
    return ingredient_to_allergen, detect_allergens_rule_based

if __name__ == "__main__":
    mapping, detector = create_allergen_mapping()
