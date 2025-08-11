# SuperBoost AllerScan

**Sistem Deteksi Alergen Makanan Berbasis Machine Learning**

Sistem deteksi alergen makanan menggunakan algoritma SVM + AdaBoost dengan akurasi 93.7%

---

## Tentang Proyek

SuperBoost AllerScan adalah aplikasi web untuk deteksi alergen makanan berbasis machine learning menggunakan algoritma **Support Vector Machine (SVM) + AdaBoost**. Sistem ini dapat menganalisis komposisi bahan makanan dan memprediksi keberadaan alergen dengan tingkat akurasi **93.7%**.

### Fitur Utama
- Multi-allergen detection: Deteksi simultan 23+ jenis alergen
- Confidence score: Tingkat kepercayaan prediksi 0-100%
- Dashboard analitik: Visualisasi data training dan prediksi  
- Export functionality: Export hasil ke Excel/CSV
- Responsive design: Interface modern dengan TailwindCSS

### Stack Teknologi
- **Backend**: FastAPI (Python), MySQL via XAMPP
- **Frontend**: React 18+, TailwindCSS, Vite
- **Machine Learning**: scikit-learn, SVM + AdaBoost
- **Database**: MySQL 8.0+ dengan SQLAlchemy ORM

## Prasyarat Sistem

- **Python**: 3.10 atau lebih tinggi
- **Node.js**: 18.0 atau lebih tinggi
- **XAMPP**: Untuk MySQL server (recommended)

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN
```

### 2. Setup XAMPP
- Download dan install XAMPP dari https://www.apachefriends.org/
- Start **Apache** dan **MySQL** services dari XAMPP Control Panel

### 3. Setup Backend
```bash
cd backend

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database (pastikan XAMPP MySQL sudah berjalan)
python ../scripts/setup_mysql.py
```

### 4. Setup Frontend
```bash
cd frontend
npm install
```

### 5. Menjalankan Aplikasi

**Start Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/macOS atau venv\Scripts\activate (Windows)
python run_dev.py
```
Backend: http://localhost:8001

**Start Frontend:**
```bash
cd frontend
npm run dev
```
Frontend: http://localhost:5173

## Struktur Proyek

```
SUPERBOOST-ALLERSCAN/
├── backend/                 # FastAPI Backend
│   ├── app/                 # Application code
│   ├── requirements.txt     # Python dependencies
│   └── run_dev.py          # Development server
│
├── frontend/               # React Frontend
│   ├── src/                # Source code
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
│
├── data/raw/               # Dataset storage
├── notebooks/              # Jupyter notebooks (model development)
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── README.md              # This file
```

## Tim Pengembang

**Siska Narulita, S.Kom., S.M., M.Kom.**  
*Research Lead & Machine Learning Algorithm*
- Pengembangan konsep algoritma SVM + AdaBoost
- Implementasi notebook `deteksi_alergen.ipynb`
- Research methodology dan validasi model

**Reynard Adelard**  
*Full-Stack Web Developer*
- Implementasi web application (Frontend React + Backend FastAPI)
- System architecture dan database design
- API development dan deployment

---

Jika proyek ini bermanfaat, berikan star di GitHub!