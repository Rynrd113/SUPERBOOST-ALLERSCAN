#!/usr/bin/env python3
"""
Test script untuk fungsi parsing ingredients
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager

def test_ingredient_parsing():
    """Test fungsi parsing ingredients"""
    print("🧪 Testing ingredient parsing...")
    
    db = database_manager
    
    # Test cases
    test_cases = [
        "tepung terigu, gula pasir, mentega, vanili",
        "daging sapi, minyak zaitun, garam, lada hitam",
        "susu, telur, keju cheddar, oregano",
        "kentang, minyak sawit, bumbu balado"
    ]
    
    for i, ingredients in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: '{ingredients}'")
        result = db._parse_ingredients_smart(ingredients)
        
        print(f"  🥘 Bahan Utama: {result['bahan_utama']}")
        print(f"  🍯 Pemanis: {result['pemanis']}")
        print(f"  🛢️  Lemak/Minyak: {result['lemak_minyak']}")
        print(f"  🧂 Penyedap Rasa: {result['penyedap_rasa']}")

if __name__ == "__main__":
    test_ingredient_parsing()
