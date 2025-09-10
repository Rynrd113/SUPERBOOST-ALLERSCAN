"""
Perbaikan algoritma untuk mendeteksi alergen spesifik
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def create_allergen_specific_predictor():
    """
    Membuat predictor untuk alergen spesifik
    """
    print("=" * 60)
    print("Membuat Algoritma Deteksi Alergen Spesifik")
    print("=" * 60)
    
    # Load dataset
    dataset_path = "data/raw/Dataset Bahan Makanan & Alergen.xlsx"
    df = pd.read_excel(dataset_path)
    
    print(f"Dataset loaded: {df.shape}")
    
    # Preprocessing data untuk multi-label
    print(f"\n1. PREPROCESSING DATA:")
    
    # Fitur input (bahan-bahan)
    feature_cols = ['Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa']
    X = df[feature_cols]
    
    # Preprocessing alergen menjadi multi-label
    allergen_lists = []
    for alergen_str in df['Alergen']:
        if pd.isna(alergen_str) or alergen_str == 'Tidak Ada':
            allergens = []
        else:
            allergens = [a.strip() for a in alergen_str.split(',')]
        allergen_lists.append(allergens)
    
    # Multi-label binarizer untuk alergen
    mlb = MultiLabelBinarizer()
    y_multi = mlb.fit_transform(allergen_lists)
    
    print(f"   Fitur: {feature_cols}")
    print(f"   Alergen classes: {list(mlb.classes_)}")
    print(f"   Total allergen types: {len(mlb.classes_)}")
    
    # One-hot encoding untuk fitur
    X_encoded = pd.get_dummies(X)
    print(f"   Features after encoding: {X_encoded.shape[1]}")
    
    # Test dengan beberapa sample
    print(f"\n2. TEST ALGORITMA:")
    
    # Model untuk setiap alergen
    model = MultiOutputClassifier(
        AdaBoostClassifier(
            estimator=SVC(kernel='linear', probability=True, random_state=42),
            n_estimators=20,
            random_state=42
        )
    )
    
    # Training
    print("   Training model...")
    model.fit(X_encoded, y_multi)
    
    # Test dengan data training untuk validasi
    print("\n3. TEST DENGAN DATA TRAINING:")
    for i in range(5):
        test_input = X.iloc[i].to_dict()
        expected_allergens = allergen_lists[i]
        
        # Preprocess input
        test_df = pd.DataFrame([test_input])
        test_encoded = pd.get_dummies(test_df)
        
        # Ensure same columns as training
        for col in X_encoded.columns:
            if col not in test_encoded.columns:
                test_encoded[col] = 0
        test_encoded = test_encoded[X_encoded.columns]
        
        # Prediksi
        prediction_proba = model.predict_proba(test_encoded)
        prediction_binary = model.predict(test_encoded)
        
        # Extract hasil
        detected_allergens = []
        for j, class_name in enumerate(mlb.classes_):
            if prediction_binary[0][j] == 1:
                # Get probability dari classifier untuk class ini
                prob = prediction_proba[j][0][1] if len(prediction_proba[j][0]) > 1 else 0
                detected_allergens.append((class_name, prob))
        
        print(f"\n   Test {i+1}:")
        print(f"   Input: {test_input}")
        print(f"   Expected: {expected_allergens}")
        print(f"   Detected: {detected_allergens}")
    
    # Test dengan input user (kacang tanah)
    print(f"\n4. TEST DENGAN INPUT USER:")
    user_inputs = [
        {
            'Bahan Utama': 'kacang tanah',
            'Pemanis': 'gula', 
            'Lemak/Minyak': 'minyak',
            'Penyedap Rasa': 'garam'
        },
        {
            'Bahan Utama': 'susu',
            'Pemanis': 'tidak ada',
            'Lemak/Minyak': 'mentega', 
            'Penyedap Rasa': 'vanilla'
        }
    ]
    
    for test_input in user_inputs:
        print(f"\n   User Input: {test_input}")
        
        # Find similar ingredients in training data
        similar_found = False
        for train_idx, row in X.iterrows():
            if any(ingredient.lower() in str(row['Bahan Utama']).lower() 
                   for ingredient in test_input['Bahan Utama'].split()):
                print(f"   Similar training data: {row.to_dict()}")
                print(f"   -> Expected allergens: {allergen_lists[train_idx]}")
                similar_found = True
                break
        
        if not similar_found:
            print("   No similar training data found - OOV detected")

if __name__ == "__main__":
    create_allergen_specific_predictor()
