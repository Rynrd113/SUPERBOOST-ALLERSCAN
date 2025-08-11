#!/usr/bin/env python3
"""
Script untuk memverifikasi API supported allergens
"""

import requests
import json

def test_supported_allergens():
    """Test supported allergens endpoint"""
    url = "http://localhost:8001/api/v1/predict/supported-allergens"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            print("🎯 SUPPORTED ALLERGENS API TEST")
            print("=" * 50)
            print(f"✅ Status: {data.get('success', False)}")
            print(f"📊 Total allergens: {data.get('total_count', 0)}")
            print(f"🤖 Model loaded: {data.get('model_info', {}).get('loaded', False)}")
            
            print("\n🏷️ Supported Allergens:")
            allergens = data.get('supported_allergens', [])
            for i, allergen in enumerate(allergens, 1):
                formatted_name = allergen.replace('_', ' ').title()
                print(f"  {i:2d}. {allergen} ({formatted_name})")
            
            print(f"\n✅ API test successful - {len(allergens)} allergens available")
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_supported_allergens()
