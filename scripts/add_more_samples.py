#!/usr/bin/env python3
"""
Additional diverse samples for better testing
"""

import requests
import json
import time

API_BASE_URL = 'http://localhost:8001'
PREDICT_ENDPOINT = f'{API_BASE_URL}/api/v1/predict/'

ADDITIONAL_SAMPLES = [
    {
        "nama_produk_makanan": "Pasta Carbonara",
        "bahan_utama": "Pasta, Telur, Keju Parmesan",
        "pemanis": "Tidak Ada", 
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Lada Hitam, Garam",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Sate Ayam",
        "bahan_utama": "Daging Ayam",
        "pemanis": "Gula Merah",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Bumbu Kacang",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Salmon Teriyaki",
        "bahan_utama": "Ikan Salmon",
        "pemanis": "Mirin, Gula",
        "lemak_minyak": "Minyak Wijen",
        "penyedap_rasa": "Kecap Asin, Jahe",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Cheese Burger",
        "bahan_utama": "Roti Burger, Keju, Daging Sapi",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Selada, Tomat, Saus",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Tom Yum Kung",
        "bahan_utama": "Udang, Jamur",
        "pemanis": "Gula Kelapa",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Serai, Cabai, Jeruk Nipis",
        "alergen": "",
        "confidence_threshold": 0.7
    }
]

def add_more_samples():
    print("🚀 ADDING MORE DIVERSE SAMPLES...")
    
    for sample in ADDITIONAL_SAMPLES:
        try:
            print(f"\n🔄 Processing: {sample['nama_produk_makanan']}")
            
            response = requests.post(
                PREDICT_ENDPOINT,
                json=sample,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    detected = result.get('detected_allergens', [])
                    print(f"✅ Success: {len(detected)} allergens detected")
                    if detected:
                        allergen_names = [a.get('name', '') for a in detected]
                        print(f"   Allergens: {', '.join(allergen_names)}")
                else:
                    print(f"❌ Error: {result.get('message', 'Unknown')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
            
            time.sleep(1)  # Delay between requests
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    add_more_samples()
    print("\n✅ Additional samples completed!")
