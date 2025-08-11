#!/usr/bin/env python3
"""
🔧 Fix Historical Confidence Data
Fix confidence values for historical data that has low confidence for "no allergens detected" cases

This script will:
1. Identify records with allergen_count = 0 but confidence < 0.5
2. Update these to have confidence = 0.95 (95%) which is correct for "no allergens"
3. Preserve original data for allergen-containing products
"""

import sys
sys.path.append('backend')

from backend.app.database.allergen_database import database_manager
from sqlalchemy import text

def fix_historical_confidence():
    """Fix historical low confidence data for no-allergen products"""
    print("🔧 FIXING HISTORICAL CONFIDENCE DATA")
    print("=" * 50)
    
    try:
        with database_manager.engine.connect() as conn:
            # First, check how many records need fixing
            check_result = conn.execute(text("""
                SELECT COUNT(*) as count
                FROM user_predictions 
                WHERE allergen_count = 0 AND confidence_score < 0.5
            """))
            
            records_to_fix = check_result.scalar()
            print(f"📊 Found {records_to_fix} records with low confidence for no-allergen products")
            
            if records_to_fix == 0:
                print("✅ No records need fixing")
                return
            
            # Show some examples before fixing
            examples = conn.execute(text("""
                SELECT product_name, confidence_score, allergen_count, created_at
                FROM user_predictions 
                WHERE allergen_count = 0 AND confidence_score < 0.5
                ORDER BY created_at DESC
                LIMIT 5
            """)).fetchall()
            
            print("\n🔍 Examples of records to be fixed:")
            for i, row in enumerate(examples, 1):
                print(f"  {i}. {row[0]} - {row[1]*100:.1f}% confidence - {row[3]}")
            
            # Ask for confirmation
            print(f"\n❓ Fix {records_to_fix} historical records?")
            print("   This will set confidence to 95% for products with no allergens detected")
            response = input("   Continue? (y/N): ").strip().lower()
            
            if response != 'y':
                print("❌ Operation cancelled")
                return
            
            # Fix the records
            print(f"\n🔄 Fixing {records_to_fix} records...")
            
            update_result = conn.execute(text("""
                UPDATE user_predictions 
                SET confidence_score = 0.95,
                    risk_level = 'none'
                WHERE allergen_count = 0 AND confidence_score < 0.5
            """))
            
            conn.commit()
            
            print(f"✅ Successfully updated {update_result.rowcount} records")
            
            # Verify the fix
            verify_result = conn.execute(text("""
                SELECT COUNT(*) as count
                FROM user_predictions 
                WHERE allergen_count = 0 AND confidence_score < 0.5
            """)).scalar()
            
            if verify_result == 0:
                print("✅ Verification successful - no more low confidence records for no-allergen products")
                
                # Show some updated examples
                updated_examples = conn.execute(text("""
                    SELECT product_name, confidence_score, allergen_count, created_at
                    FROM user_predictions 
                    WHERE allergen_count = 0 AND confidence_score >= 0.9
                    ORDER BY created_at DESC
                    LIMIT 5
                """)).fetchall()
                
                print("\n📊 Updated records (samples):")
                for i, row in enumerate(updated_examples, 1):
                    print(f"  {i}. {row[0]} - {row[1]*100:.1f}% confidence - {row[3]}")
                
            else:
                print(f"⚠️ Still have {verify_result} records that need fixing")
            
    except Exception as e:
        print(f"❌ Error fixing historical confidence: {e}")
        raise

if __name__ == "__main__":
    fix_historical_confidence()
