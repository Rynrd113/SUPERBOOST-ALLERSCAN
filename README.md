# SuperBoost AllerScan

**Sistem Deteksi Alergen Makanan Berbasis Machine Learning**

Deteksi alergen makanan menggunakan algoritma SVM + AdaBoost dengan akurasi 93.7%

---

## Tentang Proyek

**SuperBoost AllerScan** adalah sistem deteksi alergen makanan berbasis kecerdasan buatan yang dikembangkan menggunakan algoritma **SVM (Support Vector Machine) + AdaBoost**. Sistem ini mampu menganalisis komposisi makanan dan memprediksi keberadaan alergen dengan tingkat akurasi **93.7%**.

### Fitur Utama
- **Multi-Allergen Detection**: Deteksi simultan 23+ jenis alergen
- **Confidence Score**: Tingkat kepercayaan prediksi 0-100%
- **Dashboard Analitik**: Visualisasi data training dan prediksi
- **Export Functionality**: Export hasil ke Excel/CSV
- **Responsive Design**: Interface modern dengan TailwindCSS

### Teknologi
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
python scripts/setup_mysql.py
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

## API Documentation

**Interactive Documentation**: http://localhost:8001/docs

### Endpoint Utama
```http
POST /api/v1/predict              # Prediksi alergen
GET  /api/v1/dataset              # Dataset dengan pagination  
GET  /api/v1/dataset/export/excel # Export ke Excel
```

## Dokumentasi Lengkap

Untuk informasi detail, lihat dokumentasi di folder `docs/`:

- **[Installation Guide](docs/INSTALLATION.md)** - Panduan instalasi lengkap
- **[API Documentation](docs/API.md)** - Dokumentasi API detail
- **[Configuration](docs/CONFIGURATION.md)** - Konfigurasi sistem
- **[Development Guide](docs/DEVELOPMENT.md)** - Panduan development
- **[Deployment](docs/DEPLOYMENT.md)** - Panduan deployment
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Pemecahan masalah

## Tim Pengembang

### Konsep dan Algoritma Machine Learning
**Siska Narulita, S.Kom., S.M., M.Kom.**  
*Dosen Pembimbing dan Research Lead*
- Pengembangan konsep algoritma SVM + AdaBoost
- Implementasi notebook `deteksi_alergen.ipynb`
- Research methodology dan validasi model

### Web Application Development  
**Reynard Adelard**  
*Full-Stack Developer*
- Implementasi web application (Frontend React + Backend FastAPI)
- System architecture dan database design
- API development dan deployment

## Kontribusi

Kami menghargai kontribusi dari komunitas! Lihat [CONTRIBUTING.md](docs/CONTRIBUTING.md) untuk panduan kontribusi.

## Lisensi

Proyek ini dilisensikan under MIT License. Lihat [LICENSE](LICENSE) untuk detail.

---

**SuperBoost AllerScan** - Machine Learning Research Project

Jika proyek ini bermanfaat, berikan star di GitHub!