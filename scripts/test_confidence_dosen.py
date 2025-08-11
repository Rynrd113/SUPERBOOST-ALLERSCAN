#!/usr/bin/env python3
"""
🔍 Test Confidence Calculation Script
Memverifikasi bahwa perhitungan confidence sesuai dengan notebook deteksi_alergen.ipynb
"""

import sys
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Add backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def load_model_reference():
    """Memuat model referensi dari notebook"""
    print("🤖 Memuat model referensi dari notebook...")
    
    # Load dataset
    file_path = 'data/raw/Dataset Bahan Makanan & Alergen.xlsx'
    df = pd.read_excel(file_path, sheet_name='Dataset')
    
    print(f"📊 Dataset shape: {df.shape}")
    print(f"🎯 Target distribution: {df['Prediksi'].value_counts().to_dict()}")
    
    # Memilih fitur dan target sesuai notebook referensi
    fitur = ['Nama Produk Makanan', 'Bahan Utama', 'Pemanis', 'Lemak/Minyak', 'Penyedap Rasa', 'Alergen']
    target = 'Prediksi'
    
    X = df[fitur]
    y = df[target]
    
        # Transformasi sesuai notebook referensi
    X_encoded = pd.get_dummies(X)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"🔢 Features after encoding: {X_encoded.shape[1]}")
    print(f"📋 Labels: {le.classes_}")
    
    # Model sesuai notebook referensi
    svm_base = SVC(kernel='linear', probability=True, random_state=42)
    model = AdaBoostClassifier(estimator=svm_base, n_estimators=50, random_state=42)
    model.fit(X_encoded, y_encoded)
    
    print("✅ Model berhasil dilatih")
    return model, le, X_encoded

def test_confidence_calculation():
    """Test perhitungan confidence sesuai notebook referensi"""
    
    print("🧪 TESTING CONFIDENCE CALCULATION SESUAI NOTEBOOK REFERENSI")
    print("=" * 60)
    
    try:
        model, label_encoder, X_encoded = load_model_reference()

def test_confidence_calculation():
    """Test perhitungan confidence sesuai script dosen"""
    print("=" * 60)
    print("🧪 TESTING CONFIDENCE CALCULATION SESUAI SCRIPT DOSEN")
    print("=" * 60)
    
    try:
        # Load model
        model, label_encoder, X_encoded = load_model_reference()
        
        # Test data: Roti (sesuai dengan kasus user)
        test_cases = [
            {
                'Nama Produk Makanan': 'Roti',
                'Bahan Utama': 'tepung terigu',
                'Pemanis': 'gula pasir', 
                'Lemak/Minyak': 'mentega',
                'Penyedap Rasa': 'vanila',
                'Alergen': ''
            },
            {
                'Nama Produk Makanan': 'Pizza',
                'Bahan Utama': 'tepung gandum',
                'Pemanis': 'tidak ada',
                'Lemak/Minyak': 'minyak zaitun',
                'Penyedap Rasa': 'oregano',
                'Alergen': ''
            },
            {
                'Nama Produk Makanan': 'Kacang Almond', # This should exist in training data
                'Bahan Utama': 'Kacang Almond',
                'Pemanis': 'Gula Pasir',
                'Lemak/Minyak': 'Mentega',
                'Penyedap Rasa': 'Garam',
                'Alergen': 'Kacang-kacangan'
            }
        ]
        
        for i, test_data in enumerate(test_cases, 1):
            print(f"\n🧪 Test Case {i}: {test_data['Nama Produk Makanan']}")
            print(f"   Bahan: {test_data['Bahan Utama']}, {test_data['Pemanis']}, {test_data['Lemak/Minyak']}, {test_data['Penyedap Rasa']}")
            
            # Create DataFrame sesuai script dosen
            df_baru = pd.DataFrame([test_data])
            
            # One-hot encoding sesuai script dosen
            df_baru_encoded = pd.get_dummies(df_baru)
            
            # Sinkronisasi kolom sesuai script dosen
            for col in X_encoded.columns:
                if col not in df_baru_encoded.columns:
                    df_baru_encoded[col] = 0
            
            df_baru_encoded = df_baru_encoded[X_encoded.columns]
            
            # Analisis OOV
            non_zero_features = (df_baru_encoded != 0).sum().sum()
            total_features = df_baru_encoded.shape[0] * df_baru_encoded.shape[1]
            recognition_rate = (non_zero_features / total_features) * 100
            
            print(f"   🔍 Feature analysis: {non_zero_features}/{total_features} non-zero ({recognition_rate:.1f}% recognized)")
            
            # Prediksi sesuai script dosen
            prediksi = model.predict(df_baru_encoded)
            probabilitas = model.predict_proba(df_baru_encoded)
            
            # Konversi hasil sesuai script dosen
            hasil_target = label_encoder.inverse_transform(prediksi)
            akurasi_prediksi_dosen = round(probabilitas[0][prediksi[0]] * 100, 2)
            
            print(f"   📊 Script Dosen Results:")
            print(f"      Prediksi: {hasil_target[0]}")
            print(f"      Akurasi (%): {akurasi_prediksi_dosen}%")
            print(f"      Probabilitas: {probabilitas[0]}")
            print(f"      Raw confidence: {probabilitas[0][prediksi[0]]:.4f}")
            
            # Bandingkan dengan logika frontend/backend current
            if hasil_target[0] == "Tidak Mengandung Alergen":
                print(f"   🤔 Analysis:")
                print(f"      - Model dosen: {akurasi_prediksi_dosen}% confidence")
                print(f"      - Frontend logic: 95% confidence (for no allergens)")
                print(f"      - Backend logic: {akurasi_prediksi_dosen}% confidence (OOV adjusted)")
                
                if akurasi_prediksi_dosen < 50:
                    print(f"      ⚠️ INCONSISTENCY: Model gives {akurasi_prediksi_dosen}% but UI shows high confidence!")
                    print(f"      🔧 This explains the discrepancy!")
            else:
                print(f"   ✅ Allergen detected with {akurasi_prediksi_dosen}% confidence")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def analyze_model_behavior():
    """Analisis perilaku model untuk input yang tidak dikenal"""
    print("\n" + "=" * 60)
    print("🔍 ANALYZING MODEL BEHAVIOR FOR UNKNOWN INPUTS")
    print("=" * 60)
    
    try:
        model, label_encoder, X_encoded = load_model_reference()
        
        # Test completely unknown data vs known data
        unknown_data = {
            'Nama Produk Makanan': 'Produk Tidak Dikenal',
            'Bahan Utama': 'Bahan Tidak Dikenal',
            'Pemanis': 'Pemanis Tidak Dikenal',
            'Lemak/Minyak': 'Minyak Tidak Dikenal',
            'Penyedap Rasa': 'Rasa Tidak Dikenal',
            'Alergen': 'Alergen Tidak Dikenal'
        }
        
        # Process unknown data
        df_unknown = pd.DataFrame([unknown_data])
        df_unknown_encoded = pd.get_dummies(df_unknown)
        
        for col in X_encoded.columns:
            if col not in df_unknown_encoded.columns:
                df_unknown_encoded[col] = 0
        
        df_unknown_encoded = df_unknown_encoded[X_encoded.columns]
        
        # Check if it's all zeros
        non_zero = (df_unknown_encoded != 0).sum().sum()
        total = df_unknown_encoded.shape[0] * df_unknown_encoded.shape[1]
        
        print(f"🔍 Unknown data analysis:")
        print(f"   Non-zero features: {non_zero}/{total}")
        print(f"   All zeros? {non_zero == 0}")
        
        # Predict
        pred_unknown = model.predict(df_unknown_encoded)
        prob_unknown = model.predict_proba(df_unknown_encoded)
        result_unknown = label_encoder.inverse_transform(pred_unknown)
        
        print(f"\n📊 Unknown data results:")
        print(f"   Prediction: {result_unknown[0]}")
        print(f"   Confidence: {prob_unknown[0][pred_unknown[0]] * 100:.2f}%")
        print(f"   Probabilities: {prob_unknown[0]}")
        
        print(f"\n🎯 CONCLUSION:")
        if non_zero == 0:
            print("   - Semua input yang tidak dikenal menjadi vector zero setelah one-hot encoding")
            print("   - Model memberikan prediksi yang sama untuk semua zero vector")
            print(f"   - Confidence: {prob_unknown[0][pred_unknown[0]] * 100:.2f}% (ini bukan confidence yang tinggi untuk 'no allergens')")
            print("   - Frontend mengasumsikan confidence tinggi untuk 'no allergens' (95%)")
            print("   - Inilah sumber inconsistency antara hasil analisis dan tabel dataset!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_confidence_calculation()
    analyze_model_behavior()
