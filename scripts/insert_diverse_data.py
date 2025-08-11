#!/usr/bin/env python3
"""
Insert Diverse Sample Data for AllerScan Dataset - Clean Architecture
================================================================

Adds diverse prediction results with:
- High, medium, and low confidence scores
- Various allergen detection results (detected/not detected)  
- Different risk levels
- Realistic food products with ingredients

Following DRY principle and clean code practices.
Uses the proper AllergenDatabaseManager for clean architecture.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add backend path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager

# Sample data with diverse results
DIVERSE_SAMPLE_DATA = [
    {
        "nama_produk_makanan": "Pizza Margherita",
        "bahan_utama": "Tepung Gandum, Keju Mozzarella",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Zaitun",
        "penyedap_rasa": "Oregano, Basil",
        "detected_allergens": ["gandum", "susu"],
        "confidence_score": 0.95,
        "risk_level": "high",
        "allergen_count": 2
    },
    {
        "nama_produk_makanan": "Salad Buah Segar",
        "bahan_utama": "Apel, Jeruk, Anggur",
        "pemanis": "Madu",
        "lemak_minyak": "Tidak Ada", 
        "penyedap_rasa": "Tidak Ada",
        "detected_allergens": [],
        "confidence_score": 0.98,
        "risk_level": "none",
        "allergen_count": 0
    },
    {
        "nama_produk_makanan": "Cookies Kacang Almond",
        "bahan_utama": "Tepung, Kacang Almond",
        "pemanis": "Gula Brown",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Vanilla Extract",
        "detected_allergens": ["gandum", "almond", "susu"],
        "confidence_score": 0.87,
        "risk_level": "high", 
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Sup Ayam Jagung",
        "bahan_utama": "Ayam, Jagung Manis",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Garam, Lada",
        "detected_allergens": [],
        "confidence_score": 0.92,
        "risk_level": "none",
        "allergen_count": 0
    },
    {
        "nama_produk_makanan": "Smoothie Kedelai",
        "bahan_utama": "Susu Kedelai, Pisang",
        "pemanis": "Madu",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada", 
        "detected_allergens": ["kedelai"],
        "confidence_score": 0.64,
        "risk_level": "medium",
        "allergen_count": 1
    },
    {
        "nama_produk_makanan": "Roti Gandum Utuh",
        "bahan_utama": "Tepung Gandum Utuh",
        "pemanis": "Gula Aren",
        "lemak_minyak": "Minyak Canola",
        "penyedap_rasa": "Garam, Ragi",
        "detected_allergens": ["gandum"],
        "confidence_score": 0.91,
        "risk_level": "medium",
        "allergen_count": 1
    },
    {
        "nama_produk_makanan": "Omelet Keju",
        "bahan_utama": "Telur Ayam, Keju Cheddar",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Garam, Merica",
        "detected_allergens": ["telur", "susu"],
        "confidence_score": 0.96,
        "risk_level": "high",
        "allergen_count": 2
    },
    {
        "nama_produk_makanan": "Nasi Goreng Seafood",
        "bahan_utama": "Nasi, Udang, Cumi",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Sayur",
        "penyedap_rasa": "Kecap Manis, Bawang",
        "detected_allergens": ["udang", "cumi", "kedelai"],
        "confidence_score": 0.89,
        "risk_level": "high",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Yogurt Plain",
        "bahan_utama": "Susu Sapi, Kultur Bakteri",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada",
        "detected_allergens": ["susu"],
        "confidence_score": 0.94,
        "risk_level": "medium",
        "allergen_count": 1
    },
    {
        "nama_produk_makanan": "Salad Caesar",
        "bahan_utama": "Lettuce Romaine, Keju Parmesan",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Saus Caesar",
        "penyedap_rasa": "Croutons, Lemon",
        "detected_allergens": ["susu", "gandum"],
        "confidence_score": 0.73,
        "risk_level": "medium",
        "allergen_count": 2
    },
    {
        "nama_produk_makanan": "Es Krim Vanilla",
        "bahan_utama": "Susu, Krim",
        "pemanis": "Gula Putih",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Vanilla Extract",
        "detected_allergens": ["susu"],
        "confidence_score": 0.97,
        "risk_level": "medium",
        "allergen_count": 1
    },
    {
        "nama_produk_makanan": "Tuna Sandwich",
        "bahan_utama": "Roti Tawar, Tuna Kaleng",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Mayonnaise",
        "penyedap_rasa": "Selada, Tomat",
        "detected_allergens": ["gandum", "ikan", "telur"],
        "confidence_score": 0.85,
        "risk_level": "high",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Jus Alpukat Murni",
        "bahan_utama": "Alpukat Segar",
        "pemanis": "Gula Palm",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Tidak Ada",
        "detected_allergens": [],
        "confidence_score": 0.99,
        "risk_level": "none",
        "allergen_count": 0
    },
    {
        "nama_produk_makanan": "Kue Brownies Coklat",
        "bahan_utama": "Tepung, Coklat Dark",
        "pemanis": "Gula Halus",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Vanilla, Garam",
        "detected_allergens": ["gandum", "susu", "telur"],
        "confidence_score": 0.88,
        "risk_level": "high",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Mie Ayam Bakso",
        "bahan_utama": "Mie, Daging Ayam",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Wijen",
        "penyedap_rasa": "Kecap Asin, MSG",
        "detected_allergens": ["gandum", "wijen", "kedelai"],
        "confidence_score": 0.79,
        "risk_level": "medium",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Trail Mix Kacang",
        "bahan_utama": "Kacang Mete, Almond, Kenari",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Garam Laut",
        "detected_allergens": ["mete", "almond", "kenari"],
        "confidence_score": 0.93,
        "risk_level": "high",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Bubur Ayam",
        "bahan_utama": "Beras, Ayam Kampung",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Goreng",
        "penyedap_rasa": "Bawang Goreng, Seledri",
        "detected_allergens": [],
        "confidence_score": 0.89,
        "risk_level": "none",
        "allergen_count": 0
    },
    {
        "nama_produk_makanan": "Pancake Susu",
        "bahan_utama": "Tepung Terigu, Susu Cair",
        "pemanis": "Madu Murni",
        "lemak_minyak": "Mentega Tawar",
        "penyedap_rasa": "Vanilla Extract",
        "detected_allergens": ["gandum", "susu", "telur"],
        "confidence_score": 0.91,
        "risk_level": "high",
        "allergen_count": 3
    },
    {
        "nama_produk_makanan": "Keripik Kentang",
        "bahan_utama": "Kentang Segar",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Minyak Kelapa Sawit",
        "penyedap_rasa": "Garam, Bumbu BBQ",
        "detected_allergens": [],
        "confidence_score": 0.86,
        "risk_level": "none",
        "allergen_count": 0
    },
    {
        "nama_produk_makanan": "Sushi Salmon",
        "bahan_utama": "Nasi Sushi, Salmon Segar",
        "pemanis": "Tidak Ada",
        "lemak_minyak": "Tidak Ada",
        "penyedap_rasa": "Nori, Wasabi",
        "detected_allergens": ["ikan"],
        "confidence_score": 0.68,
        "risk_level": "medium",
        "allergen_count": 1
    }
]

def insert_diverse_data():
    """Insert diverse sample data into the database using clean architecture"""
    print("🚀 INSERTING DIVERSE SAMPLE DATA...")
    
    try:
        # Use the clean database manager
        db = database_manager
        
        # Add current timestamp variation for realistic data
        base_time = datetime.now()
        
        for i, sample in enumerate(DIVERSE_SAMPLE_DATA):
            # Create realistic timestamp (spread over last 30 days)
            created_time = base_time - timedelta(days=30-i, hours=i*2, minutes=i*5)
            
            # Format detected allergens as string
            allergens_str = ", ".join(sample["detected_allergens"]) if sample["detected_allergens"] else "tidak terdeteksi"
            
            # Create ingredients string
            ingredients = f"{sample['bahan_utama']}, {sample['pemanis']}, {sample['lemak_minyak']}, {sample['penyedap_rasa']}"
            ingredients = ingredients.replace(", Tidak Ada", "").replace("Tidak Ada, ", "").replace("Tidak Ada", "")
            
            # Determine detection status
            detection_status = "Terdeteksi" if sample["allergen_count"] > 0 else "Tidak Terdeteksi"
            
            # Create proper prediction data structure for clean architecture
            prediction_data = {
                "productName": sample["nama_produk_makanan"],
                "ingredients": ingredients,
                "allergens": allergens_str,
                "allergen_count": sample["allergen_count"],
                "confidence": sample["confidence_score"],
                "risk_level": sample["risk_level"],
                "processing_time_ms": round((0.05 + (i * 0.01)) * 1000, 1),  # Convert to ms
                "model_version": "SVM+AdaBoost-v2.1",
                "user_ip": "127.0.0.1",
                "user_agent": "DataInsertionScript/1.0"
            }
            
            # Save to database using clean architecture method
            result_id = db.save_prediction_result(prediction_data)
            
            print(f"✅ Inserted: {sample['nama_produk_makanan']} (ID: {result_id})")
            print(f"   Allergens: {allergens_str} | Confidence: {sample['confidence_score']*100:.1f}% | Risk: {sample['risk_level']}")
        
        print(f"\n🎉 Successfully inserted {len(DIVERSE_SAMPLE_DATA)} diverse records!")
        
        # Print statistics
        print("\n📊 DATA DISTRIBUTION:")
        risk_counts = {}
        detection_counts = {"detected": 0, "not_detected": 0}
        confidence_ranges = {"high": 0, "medium": 0, "low": 0}
        
        for sample in DIVERSE_SAMPLE_DATA:
            # Risk level distribution
            risk_level = sample["risk_level"]
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
            
            # Detection distribution
            if sample["allergen_count"] > 0:
                detection_counts["detected"] += 1
            else:
                detection_counts["not_detected"] += 1
            
            # Confidence distribution
            confidence = sample["confidence_score"]
            if confidence >= 0.85:
                confidence_ranges["high"] += 1
            elif confidence >= 0.70:
                confidence_ranges["medium"] += 1
            else:
                confidence_ranges["low"] += 1
        
        print(f"Risk Levels: {risk_counts}")
        print(f"Detection: Detected={detection_counts['detected']}, Not Detected={detection_counts['not_detected']}")
        print(f"Confidence: High={confidence_ranges['high']}, Medium={confidence_ranges['medium']}, Low={confidence_ranges['low']}")
        
    except Exception as e:
        print(f"❌ Error inserting data: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = insert_diverse_data()
    if success:
        print("\n✅ Diverse sample data insertion completed successfully!")
    else:
        print("\n❌ Failed to insert diverse sample data!")
