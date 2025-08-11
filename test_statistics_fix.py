#!/usr/bin/env python3
"""
🧪 Test Dataset Statistics API Endpoints

Test script untuk memverifikasi bahwa perbaikan statistik dataset bekerja dengan baik.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api/v1"

def test_dataset_predictions():
    """Test paginated predictions endpoint"""
    print("🧪 Testing Dataset Predictions Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/dataset/predictions", params={
            'page': 1,
            'limit': 10,
            'include_stats': True
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Predictions endpoint working")
            
            if 'data' in data:
                predictions = data['data'].get('predictions', [])
                pagination = data['data'].get('pagination', {})
                
                print(f"📄 Retrieved {len(predictions)} predictions")
                print(f"📊 Total items: {pagination.get('total_items', 'N/A')}")
                print(f"📈 Current page: {pagination.get('current_page', 'N/A')}")
                
                return True
            else:
                print("❌ Invalid response format")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_dataset_statistics():
    """Test comprehensive statistics endpoint"""
    print("\n🧪 Testing Dataset Statistics Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/dataset/statistics")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics endpoint working")
            
            if 'data' in data:
                stats_data = data['data']
                overview = stats_data.get('overview', {})
                
                print(f"📊 Total predictions: {overview.get('total_predictions', 'N/A')}")
                print(f"📈 Detection rate: {overview.get('detection_rate', 'N/A')}%")
                print(f"🎯 Average confidence: {overview.get('average_confidence', 'N/A')}%")
                
                # Check chart data
                chart_data = stats_data.get('chart_data', {})
                detection_pie = chart_data.get('detection_pie', [])
                allergens_dist = chart_data.get('allergens_distribution', [])
                
                print(f"📊 Detection breakdown: {len(detection_pie)} categories")
                print(f"🥜 Allergen types: {len(allergens_dist)} different allergens")
                
                # Show detection breakdown
                for item in detection_pie:
                    print(f"  - {item.get('name', 'Unknown')}: {item.get('count', 0)}")
                
                return True
            else:
                print("❌ Invalid response format")
                print(f"Response: {json.dumps(data, indent=2)[:500]}")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def compare_data_consistency():
    """Compare data consistency between endpoints"""
    print("\n🔍 Testing Data Consistency...")
    
    # Get predictions data
    pred_response = requests.get(f"{API_BASE}/dataset/predictions", params={
        'page': 1, 'limit': 50, 'include_stats': True
    })
    
    # Get statistics data  
    stats_response = requests.get(f"{API_BASE}/dataset/statistics")
    
    if pred_response.status_code == 200 and stats_response.status_code == 200:
        pred_data = pred_response.json()
        stats_data = stats_response.json()
        
        # Extract totals
        pagination_total = pred_data.get('data', {}).get('pagination', {}).get('total_items', 0)
        stats_total = stats_data.get('data', {}).get('overview', {}).get('total_predictions', 0)
        
        print(f"📄 Pagination total: {pagination_total}")
        print(f"📊 Statistics total: {stats_total}")
        
        if pagination_total == stats_total:
            print("✅ Data consistency: PASS")
            return True
        else:
            print("❌ Data consistency: FAIL - Totals don't match!")
            return False
    else:
        print("❌ Could not get data from both endpoints")
        return False

def main():
    """Main test runner"""
    print("🚀 Starting Dataset Statistics Fix Verification")
    print("=" * 60)
    
    results = []
    
    # Test individual endpoints
    results.append(test_dataset_predictions())
    results.append(test_dataset_statistics())
    results.append(compare_data_consistency())
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! Statistics fix is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()
