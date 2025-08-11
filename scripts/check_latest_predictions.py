#!/usr/bin/env python3
"""
Check Latest Database Entries After Fix
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database.allergen_database import database_manager
from sqlalchemy import text
from datetime import datetime

def check_latest_predictions():
    """Check the latest predictions in user_predictions table"""
    print("🔍 CHECKING LATEST USER PREDICTIONS...")
    
    try:
        with database_manager.engine.connect() as conn:
            # Check latest predictions
            result = conn.execute(text("""
                SELECT product_name, ingredients_input, predicted_allergens, 
                       allergen_count, confidence_score, risk_level,
                       created_at
                FROM user_predictions 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            
            predictions = result.fetchall()
            
            if predictions:
                print(f"📊 Found {len(predictions)} latest predictions:")
                for i, row in enumerate(predictions, 1):
                    print(f"\n{i}. {row[0]}")
                    print(f"   Ingredients: {row[1]}")
                    print(f"   Detected Allergens: {row[2]}")
                    print(f"   Allergen Count: {row[3]}")
                    print(f"   Confidence Score: {row[4]*100:.1f}%")
                    print(f"   Risk Level: {row[5]}")
                    print(f"   Created At: {row[6]}")
                    
                    # Check if this is the fixed case
                    if row[0] == 'Roti' and row[3] == 0 and row[4] > 0.9:
                        print(f"   ✅ FIXED! No allergens with HIGH confidence!")
                    elif row[0] == 'Roti' and row[3] == 0 and row[4] < 0.7:
                        print(f"   ⚠️ Still has the OLD issue - low confidence for no allergens")
            else:
                print("❌ No predictions found")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_latest_predictions()
