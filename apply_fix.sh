#!/bin/bash

echo "🔧 QUICK FIX: Applying AllerScan confidence & table color fixes"

# 1. Backup original predictor
cp backend/app/models/inference/predictor.py backend/app/models/inference/predictor_backup.py

# 2. Replace original predictor with fixed version  
cp backend/app/models/inference/predictor_fixed.py backend/app/models/inference/predictor.py

# 3. Update imports in predictor.py to match original structure
sed -i 's/predictor_fixed as predictor/predictor/g' backend/app/models/inference/predictor.py
sed -i 's/AllergenPredictorFixed/AllergenPredictor/g' backend/app/models/inference/predictor.py 
sed -i 's/predictor_fixed/predictor/g' backend/app/models/inference/predictor.py

echo "✅ Fixes applied successfully!"
echo "🔄 Restart your backend server to see the changes"
echo ""
echo "📊 Expected results:"
echo "  - Unknown input: ~12% confidence" 
echo "  - Partially known: 24-57% confidence"
echo "  - Well-known input: 57%+ confidence"
echo "  - Table colors: Yellow for detected, Green for not detected"
