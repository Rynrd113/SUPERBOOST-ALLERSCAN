# 📂 Scripts Directory Structure

Direktori ini berisi script-script utilitas yang terorganisasi berdasarkan fungsi.

## 📊 Data Management (`data_management/`)
Script untuk mengelola dan memasukkan data ke sistem.

- **`add_more_samples.py`** - Menambahkan sample data tambahan
- **`insert_diverse_data.py`** - Memasukkan data yang beragam untuk testing
- **`insert_samples_via_api.py`** - Memasukkan data melalui API endpoint

## 🔧 Maintenance (`maintenance/`)
Script untuk pemeliharaan dan debugging sistem.

- **`debug_database_values.py`** - Debug nilai-nilai dalam database
- **`fix_historical_confidence.py`** - Perbaiki confidence score historis

## 🧪 Testing (`testing/`)  
Script untuk testing berbagai komponen sistem.

- **`test_confidence_dosen.py`** - Test sesuai dengan script referensi dosen
- **`test_confidence_fix.py`** - Test perbaikan consistency confidence
- **`test_form_submission.py`** - Test pengiriman form
- **`test_ingredient_parsing.py`** - Test parsing ingredient
- **`test_supported_allergens.py`** - Test daftar alergen yang didukung

## 📝 Logs (`logs/`)
Direktori untuk menyimpan log file dari script yang dijalankan.

## 🚀 Usage

Setiap script dapat dijalankan langsung dari root project:

```bash
# Data management
python scripts/data_management/add_more_samples.py

# Maintenance
python scripts/maintenance/debug_database_values.py

# Testing
python scripts/testing/test_confidence_dosen.py
```

## 📋 Notes

- Semua script sudah dikonfigurasi dengan path yang benar
- Script dapat dijalankan dari root directory project
- Log output disimpan di folder `logs/` jika ada
