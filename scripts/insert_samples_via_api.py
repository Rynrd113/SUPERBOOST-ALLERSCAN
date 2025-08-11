#!/usr/bin/env python3
"""
Insert Diverse Sample Data via API Endpoint
================================================================

Uses the existing predict API endpoint to insert diverse prediction results.
This ensures data consistency with the actual application flow.
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
API_BASE_URL = 'http://localhost:8001'
PREDICT_ENDPOINT = f'{API_BASE_URL}/api/v1/predict/'

# Sample data with diverse results
DIVERSE_SAMPLES = [
    {
        "nama_produk_makanan": "Pizza Margherita",
        "bahan_utama": "Tepung Gandum, Keju Mozzarella",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Zaitun",
        "penyedap_rasa": "Oregano, Basil",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Salad Buah Segar",
        "bahan_utama": "Apel, Jeruk, Anggur",
        "pemanis": "Madu",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Cookies Kacang Almond",
        "bahan_utama": "Tepung, Kacang Almond",
        "pemanis": "Gula Brown",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Vanilla Extract",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Sup Ayam Jagung",
        "bahan_utama": "Ayam, Jagung Manis",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Garam, Lada",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Smoothie Kedelai",
        "bahan_utama": "Susu Kedelai, Pisang",
        "pemanis": "Madu",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Roti Gandum Utuh",
        "bahan_utama": "Tepung Gandum Utuh",
        "pemanis": "Gula Aren",
        "lemak_minyak": "Minyak Canola",
        "penyedap_rasa": "Garam, Ragi",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Omelet Keju",
        "bahan_utama": "Telur Ayam, Keju Cheddar",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Garam, Merica",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Nasi Goreng Seafood",
        "bahan_utama": "Nasi, Udang, Cumi",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Sayur",
        "penyedap_rasa": "Kecap Manis, Bawang",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Yogurt Plain",
        "bahan_utama": "Susu Sapi, Kultur Bakteri",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada",
        "alergen": "",
        "confidence_threshold": 0.7
    },
    {
        "nama_produk_makanan": "Es Krim Vanilla",
        "bahan_utama": "Susu, Krim",
        "pemanis": "Gula Putih",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Vanilla Extract",
        "alergen": "",
        "confidence_threshold": 0.7
    }
]

def insert_sample_via_api():
    """Insert sample data via API predictions"""
    print("🚀 INSERTING DIVERSE SAMPLE DATA VIA API...")
    
    success_count = 0
    failed_count = 0
    
    for i, sample in enumerate(DIVERSE_SAMPLES):
        try:
            print(f"\n🔄 Processing: {sample['nama_produk_makanan']}")
            
            # Make API request
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
                    allergen_names = [a.get('name', '') for a in detected]
                    confidence_scores = [a.get('confidence', 0) for a in detected]
                    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                    
                    print(f"✅ Success: {len(detected)} allergens detected")
                    print(f"   Allergens: {', '.join(allergen_names) if allergen_names else 'None'}")
                    print(f"   Avg Confidence: {avg_confidence:.2f}")
                    
                    success_count += 1
                else:
                    print(f"❌ API Error: {result.get('message', 'Unknown error')}")
                    failed_count += 1
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                failed_count += 1
            
            # Small delay between requests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            failed_count += 1
            continue
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📈 Success Rate: {success_count/len(DIVERSE_SAMPLES)*100:.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    success = insert_sample_via_api()
    if success:
        print("\n🎉 Sample data insertion completed!")
    else:
        print("\n❌ Failed to insert sample data!")
