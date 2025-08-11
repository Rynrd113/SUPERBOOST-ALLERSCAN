# 🗄️ AllerScan Database Architecture

## 📋 **Single MySQL Database Implementation**

AllerScan sekarang menggunakan **HANYA MySQL** dengan struktur database yang bersih dan terpusat.

### 🏗️ **Struktur Database**

```
backend/app/database/
├── allergen_database.py    ← UTAMA: MySQL implementation
├── __init__.py            ← Database module exports  
├── README.md              ← Dokumentasi ini
└── archive/               ← Backup file lama (SQLite, MySQL deprecated)
```

### 📦 **File Utama**

#### ✅ `allergen_database.py` 
- **MySQL implementation** dengan Clean Architecture
- **AllergenDatabaseManager class** - Central database manager
- **Connection pooling** untuk performa optimal
- **MySQL tables**: `user_predictions`, `model_performance`

#### ✅ `__init__.py`
- Export `database_manager` sebagai instance utama
- Import point untuk seluruh aplikasi

### 🗂️ **Database Schema (MySQL)**

#### **Table: user_predictions**
Primary data source untuk website - History hasil prediksi form user
```sql
CREATE TABLE user_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    bahan_utama TEXT,
    pemanis VARCHAR(255) DEFAULT 'Tidak Ada',
    lemak_minyak VARCHAR(255) DEFAULT 'Tidak Ada', 
    penyedap_rasa VARCHAR(255) DEFAULT 'Tidak Ada',
    ingredients_input TEXT NOT NULL,
    predicted_allergens TEXT,
    allergen_count INT DEFAULT 0,
    confidence_score DECIMAL(5,4) DEFAULT 0.0000,
    risk_level ENUM('none', 'low', 'medium', 'high') DEFAULT 'none',
    processing_time_ms DECIMAL(8,2) DEFAULT 0.00,
    model_version VARCHAR(100) DEFAULT 'SVM+AdaBoost',
    keterangan TEXT DEFAULT 'Form input pengguna',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_ip VARCHAR(45),
    user_agent TEXT
);
```

#### **Table: model_performance** 
Tracking performa model ML
```sql
CREATE TABLE model_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_type VARCHAR(100) NOT NULL,
    accuracy DECIMAL(5,4),
    cross_validation_score DECIMAL(5,4),
    training_samples INT,
    test_samples INT,
    feature_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🔗 **Penggunaan**

#### Import Database:
```python
from app.database.allergen_database import database_manager
# atau
from app.database import db  # Same instance
```

#### Operasi Database:
```python
# Save prediction result
record_id = database_manager.save_prediction_result(prediction_data)

# Get prediction history
results = database_manager.get_prediction_history(limit=50, offset=0)

# Get statistics 
stats = database_manager.get_statistics()

# Test connection
is_connected = database_manager.test_connection()
```

### ⚙️ **Environment Variables**
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=allerscan_db
```

### 🎯 **Data Flow**
```
User Form Input → ML Model Prediction → database_manager.save_prediction_result() 
                                    ↓
                              user_predictions table
                                    ↓  
                            Website Dataset Display
```

### 🧹 **Cleanup Complete**
- ❌ `mysql_database.py` - **DIHAPUS** (redundant)  
- ❌ SQLite implementation - **DIARSIPKAN**
- ✅ Single MySQL implementation - **AKTIF**

### 📊 **Benefits**
- **DRY Principle**: Tidak ada duplikasi kode
- **Clean Architecture**: Single responsibility
- **Consistent Naming**: Struktur konsisten
- **Better Performance**: MySQL dengan connection pooling
- **Maintainable**: Satu file database untuk maintenance

---
**🚀 AllerScan MySQL Database - Production Ready**
