#!/usr/bin/env python3
"""
Test script untuk simulasi form submission dengan parsing ingredients
"""
import sys
import os
import requests
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_form_submission():
    """Test form submission dengan parsing ingredients"""
    print("🧪 Testing form submission dengan parsing...")
    
    # URL endpoint
    api_url = "http://localhost:8001/api/v1/predict/"
    
    # Test data yang sama seperti yang disebutkan user
    test_data = {
        "nama_produk_makanan": "Roti", 
        "bahan_utama": "tepung terigu",
        "pemanis": "gula pasir",
        "lemak_minyak": "mentega", 
        "penyedap_rasa": "vanili",
        "alergen": "",
        "confidence_threshold": 0.5
    }
    
    try:
        print(f"📤 Sending request to: {api_url}")
        print(f"📦 Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(api_url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📊 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_form_submission()
