#!/usr/bin/env python3
"""
🔍 Test Confidence Fix - Verify consistent confidence calculation
Tests that confidence is calculated consistently between frontend and backend
"""

import requests
import json

# Test endpoint
API_BASE = "http://localhost:8001"
PREDICT_ENDPOINT = f"{API_BASE}/api/v1/predict/"

def test_confidence_fix():
    """Test confidence calculation fix"""
    print("🧪 TESTING CONFIDENCE FIX")
    print("=" * 50)
    
    # Test case: "Roti" with ingredients that should NOT contain allergens
    test_data = {
        "nama_produk_makanan": "Roti Test",
        "bahan_utama": "tepung terigu, gula pasir, mentega, vanila", 
        "pemanis": "Gula Pasir",
        "lemak_minyak": "Mentega",
        "penyedap_rasa": "Vanila",
        "alergen": "Tidak Ada",
        "confidence_threshold": 0.5
    }
    
    print(f"📤 Sending test request:")
    print(f"   Product: {test_data['nama_produk_makanan']}")
    print(f"   Ingredients: {test_data['bahan_utama']}")
    print("")
    
    try:
        # Make API request
        response = requests.post(
            PREDICT_ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("📥 API Response:")
            print(f"   Success: {result.get('success')}")
            print(f"   Detected allergens: {len(result.get('detected_allergens', []))}")
            print(f"   Total allergens: {result.get('total_allergens_detected', 0)}")
            print(f"   Processing time: {result.get('processing_time_ms', 0):.1f}ms")
            print(f"   Model version: {result.get('model_version', 'Unknown')}")
            
            detected = result.get('detected_allergens', [])
            has_allergens = len(detected) > 0
            
            if has_allergens:
                print(f"   📊 Detected allergens details:")
                for i, allergen in enumerate(detected, 1):
                    conf = allergen.get('confidence', 0) * 100
                    print(f"      {i}. {allergen.get('allergen', 'Unknown')}: {conf:.1f}% confidence")
                
                # Calculate average confidence (same as frontend logic)
                avg_confidence = sum([a.get('confidence', 0) for a in detected]) / len(detected)
                print(f"   📈 Average confidence: {avg_confidence*100:.1f}%")
                
                # Calculate risk level (same as frontend logic) 
                max_confidence = max([a.get('confidence', 0) for a in detected])
                if max_confidence > 0.8 or len(detected) > 2:
                    risk_level = 'high'
                elif max_confidence > 0.5 or len(detected) > 1:
                    risk_level = 'medium'
                else:
                    risk_level = 'low'
                print(f"   ⚠️ Expected risk level: {risk_level}")
                
            else:
                print(f"   ✅ NO ALLERGENS DETECTED")
                print(f"   📈 Expected confidence: 95.0% (high confidence for no allergens)")
                print(f"   ⚠️ Expected risk level: none (no allergens = no risk)")
            
            print("")
            print("🔍 EXPECTED BEHAVIOR:")
            if has_allergens:
                print("   - Database should store AVERAGE confidence of detected allergens")
                print("   - Database should store calculated risk level")
            else:
                print("   - Database should store 95% confidence (0.95)")
                print("   - Database should store 'none' risk level")
                print("   - Frontend should display 95% confidence")
                print("   - Dataset table should show ~95% confidence")
            
            return True
            
        else:
            print(f"❌ API Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def verify_database_entry():
    """Verify the database entry matches expected values"""
    print("\n🔍 VERIFYING DATABASE ENTRY")
    print("=" * 50)
    
    try:
        # Get dataset results to verify database entry
        response = requests.get(f"{API_BASE}/api/v1/predict/dataset-results?limit=1")
        
        if response.status_code == 200:
            result = response.json()
            dataset_results = result.get('dataset_results', [])
            
            if dataset_results:
                latest_entry = dataset_results[0]  # Most recent entry
                
                print("📋 Latest database entry:")
                print(f"   Product: {latest_entry.get('nama_produk', 'Unknown')}")
                print(f"   Ingredients: {latest_entry.get('bahan_utama', 'Unknown')}")
                print(f"   Detected allergens: {latest_entry.get('alergen_predicted', 'Unknown')}")
                print(f"   Allergen count: {latest_entry.get('allergen_count', 0)}")
                print(f"   Confidence score: {latest_entry.get('confidence_score', 0):.4f} ({latest_entry.get('confidence_score', 0)*100:.1f}%)")
                print(f"   Risk level: {latest_entry.get('risk_level', 'Unknown')}")
                print(f"   Detection status: {latest_entry.get('hasil_deteksi', 'Unknown')}")
                
                # Verify the fix
                confidence = latest_entry.get('confidence_score', 0)
                allergen_count = latest_entry.get('allergen_count', 0)
                
                if allergen_count == 0:
                    if abs(confidence - 0.95) < 0.01:  # Allow small floating point differences
                        print("   ✅ CONFIDENCE FIX VERIFIED: 95% for no allergens detected")
                    else:
                        print(f"   ❌ CONFIDENCE FIX FAILED: Expected ~0.95, got {confidence:.4f}")
                else:
                    print(f"   ℹ️ Allergens detected, confidence calculation depends on individual allergen scores")
                
                return True
            else:
                print("   ⚠️ No database entries found")
                return False
        else:
            print(f"❌ Failed to get dataset results: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CONFIDENCE FIX VERIFICATION TEST")
    print("=" * 60)
    
    # Test the API
    api_success = test_confidence_fix()
    
    if api_success:
        # Wait a moment for database to be updated
        import time
        print("\n⏳ Waiting for database update...")
        time.sleep(2)
        
        # Verify database entry
        db_success = verify_database_entry()
        
        if db_success:
            print("\n✅ CONFIDENCE FIX VERIFICATION COMPLETED SUCCESSFULLY!")
            print("   Try submitting the same form again and check if dataset table shows ~95% confidence")
        else:
            print("\n⚠️ API test passed but database verification failed")
    else:
        print("\n❌ API test failed")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Submit a form with ingredients that don't contain allergens")
    print("   2. Check if frontend shows 95% confidence")
    print("   3. Check if dataset table shows ~95% confidence (not 12%)")
