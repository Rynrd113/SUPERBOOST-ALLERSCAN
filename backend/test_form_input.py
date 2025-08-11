#!/usr/bin/env python3
"""
Test script untuk menambahkan 5 data form baru ke database
Untuk menguji real-time update di frontend
"""

import requests
import json
import time
from datetime import datetime

# API endpoint
BASE_URL = "http://localhost:8001"
PREDICT_URL = f"{BASE_URL}/api/v1/predict/"

# Test data - 5 produk makanan yang berbeda
test_products = [
    {
        "nama_produk_makanan": "Kue Cokelat Premium",
        "bahan_utama": "tepung terigu, telur ayam, susu sapi, cokelat bubuk",
        "pemanis": "gula pasir, sirup jagung",
        "lemak_minyak": "mentega, minyak kelapa",
        "penyedap_rasa": "vanilla extract, essence cokelat",
        "alergen": ""
    },
    {
        "nama_produk_makanan": "Crackers Keju",
        "bahan_utama": "tepung gandum, keju cheddar, telur",
        "pemanis": "tidak ada",
        "lemak_minyak": "minyak sawit",
        "penyedap_rasa": "bumbu keju, garam",
        "alergen": ""
    },
    {
        "nama_produk_makanan": "Smoothie Kacang",
        "bahan_utama": "kacang almond, kacang mete, susu almond",
        "pemanis": "madu murni",
        "lemak_minyak": "tidak ada",
        "penyedap_rasa": "ekstrak vanilla",
        "alergen": ""
    },
    {
        "nama_produk_makanan": "Pasta Seafood",
        "bahan_utama": "tepung durum, udang, cumi-cumi, kerang",
        "pemanis": "tidak ada",
        "lemak_minyak": "olive oil",
        "penyedap_rasa": "bawang putih, oregano, basil",
        "alergen": ""
    },
    {
        "nama_produk_makanan": "Roti Gandum Kedelai",
        "bahan_utama": "tepung gandum utuh, tepung kedelai, telur",
        "pemanis": "gula kelapa",
        "lemak_minyak": "mentega tawar",
        "penyedap_rasa": "ekstrak ragi, garam laut",
        "alergen": ""
    }
]

def send_prediction_request(product_data):
    """Send prediction request to API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TestScript/1.0'
        }
        
        print(f"🚀 Testing product: {product_data['nama_produk_makanan']}")
        
        response = requests.post(
            PREDICT_URL,
            json=product_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('total_allergens_detected', 0)} allergens detected")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 TESTING REAL-TIME DATA UPDATE - Form Submissions")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    success_count = 0
    
    for i, product in enumerate(test_products, 1):
        print(f"\n[{i}/5] Processing...")
        
        if send_prediction_request(product):
            success_count += 1
            print(f"💾 Data saved to database")
        
        # Wait 2 seconds between requests to simulate real user input
        if i < len(test_products):
            print("⏳ Waiting 3 seconds...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✅ Test completed: {success_count}/{len(test_products)} successful")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📊 Check frontend for real-time updates!")
    print("=" * 60)

if __name__ == "__main__":
    main()
