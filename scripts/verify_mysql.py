#!/usr/bin/env python3
"""
🔍 Verify MySQL Integration for AllerScan
Tests database connection and data integrity
"""

import sys
from pathlib import Path

# Add parent directory to path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from app.database.allergen_database import database_manager as db
from app.models.inference.predictor import predictor

def test_mysql_connection():
    """Test MySQL database connection"""
    print("🔍 Testing MySQL Connection...")
    try:
        if db.test_connection():
            print("✅ MySQL connection successful!")
            return True
        else:
            print("❌ MySQL connection failed!")
            return False
    except Exception as e:
        print(f"❌ MySQL connection error: {e}")
        return False

def test_data_integrity():
    """Test data integrity in MySQL"""
    print("\n📊 Testing Data Integrity...")
    try:
        # Get statistics
        stats = db.get_statistics()
        print(f"   📋 Dataset records: {stats['dataset_records']}")
        print(f"   📝 Form test records: {stats['form_test_records']}")
        print(f"   📈 Average confidence: {stats['average_confidence']:.3f}")
        print(f"   ✅ Items with allergens detected: {stats['detected_count']}")
        print(f"   ⚪ Items with no allergens: {stats['not_detected_count']}")
        
        # Test sample data retrieval
        sample_data = db.get_dataset_with_results(limit=3)
        print(f"\n📋 Sample Dataset Records (first 3):")
        for i, record in enumerate(sample_data, 1):
            confidence = record.get('confidence_score', 0)
            print(f"   {i}. {record['nama_produk']}")
            print(f"      Confidence: {confidence:.3f} ({'N/A' if confidence == 0 else f'{confidence*100:.1f}%'})")
            print(f"      Detected: {record['alergen_predicted']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data integrity test error: {e}")
        return False

def test_ml_model():
    """Test ML model is loaded"""
    print("\n🤖 Testing ML Model...")
    try:
        if predictor.is_loaded:
            info = predictor.get_model_info()
            print(f"   ✅ Model loaded: {info['model_type']}")
            print(f"   📊 Accuracy: {info['accuracy']:.3f}")
            print(f"   🏷️ Supported allergens: {len(info['supported_allergens'])}")
            return True
        else:
            print("❌ ML model not loaded!")
            return False
    except Exception as e:
        print(f"❌ ML model test error: {e}")
        return False

def test_prediction():
    """Test a simple prediction"""
    print("\n🧪 Testing Prediction...")
    try:
        test_ingredients = "tepung terigu, telur, susu, mentega"
        detected_allergens, metadata = predictor.predict_allergens(test_ingredients)
        
        print(f"   🔍 Test input: {test_ingredients}")
        print(f"   📋 Detected allergens: {len(detected_allergens)}")
        for allergen in detected_allergens[:3]:  # Show first 3
            print(f"      - {allergen.allergen}: {allergen.confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction test error: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 AllerScan MySQL Integration Verification")
    print("=" * 50)
    
    tests = [
        ("MySQL Connection", test_mysql_connection),
        ("Data Integrity", test_data_integrity),
        ("ML Model", test_ml_model),
        ("Prediction", test_prediction)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! MySQL integration successful!")
        print("\n📋 Next steps:")
        print("   1. Frontend should now show real confidence values")
        print("   2. Dataset page should load data from MySQL")
        print("   3. Form submissions will be saved to MySQL")
        print("   4. No more 'N/A' confidence values!")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Please check configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
