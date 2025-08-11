# 🍎 SuperBoost AllerScan

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18%2B-61dafb.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4%2B-38bdf8.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AI-Powered Food Allergen Detection System**  
*Deteksi alergen makanan menggunakan algoritma SVM + AdaBoost dengan akurasi 93.7%*

[🚀 Demo](#demo) • [📖 Documentation](#dokumentasi) • [🛠️ Installation](#instalasi) • [🤝 Contributing](#kontribusi)

</div>

---

## 📋 Daftar Isi

- [🌟 Tentang Proyek](#-tentang-proyek)
- [✨ Fitur Utama](#-fitur-utama)
- [🛠️ Teknologi](#️-teknologi)
- [📊 Performa Model](#-performa-model)
- [⚙️ Instalasi](#️-instalasi)
- [🚀 Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [📁 Struktur Proyek](#-struktur-proyek)
- [🔧 Konfigurasi](#-konfigurasi)
- [📖 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [📈 Monitoring](#-monitoring)
- [🤝 Kontribusi](#-kontribusi)
- [📄 Lisensi](#-lisensi)
- [👥 Tim Pengembang](#-tim-pengembang)

---

## 🌟 Tentang Proyek

**SuperBoost AllerScan** adalah sistem deteksi alergen makanan berbasis kecerdasan buatan yang dikembangkan menggunakan algoritma **SVM (Support Vector Machine) + AdaBoost**. Sistem ini mampu menganalisis komposisi makanan dan memprediksi keberadaan alergen dengan tingkat akurasi **93.7%**.

### 🎯 Tujuan Proyek
- Membantu konsumen mengidentifikasi alergen dalam produk makanan
- Memberikan informasi keamanan pangan yang akurat dan cepat
- Mendukung keputusan konsumsi yang lebih aman bagi penderita alergi
- Meningkatkan kesadaran masyarakat tentang alergen makanan

### 🏆 Pencapaian
- ✅ **Akurasi Model**: 93.7% dengan Cross-Validation K=10
- ✅ **Response Time**: < 500ms untuk prediksi
- ✅ **Deteksi Multi-Alergen**: 23+ jenis alergen yang didukung
- ✅ **UI/UX Modern**: Responsive design dengan TailwindCSS

### 📊 **Status Proyek Terkini**
- ✅ **Frontend**: Versi stabil dengan komponen sederhana dan reliable
- ✅ **Backend**: API fully functional dengan database MySQL
- ✅ **Documentation**: Terorganisir dalam folder `docs/` 
- ✅ **File Structure**: Clean organization untuk maintainability
- ⚠️ **Development**: Kembali ke versi core functionality untuk stabilitas

> 💡 **Catatan**: Proyek ini telah melalui beberapa fase optimisasi dan saat ini menggunakan implementasi yang stabil dan mudah dipelihara. Dokumentasi lengkap tersedia di folder `docs/`.

---

## ✨ Fitur Utama

### 🔍 Deteksi Alergen Cerdas
- **Multi-Allergen Detection**: Deteksi simultan 23+ jenis alergen
- **Confidence Score**: Tingkat kepercayaan prediksi 0-100%
- **Risk Assessment**: Klasifikasi risiko (None, Medium, High)
- **Real-time Analysis**: Hasil prediksi instan dalam hitungan detik

### 📊 Dashboard Analitik
- **Dataset Statistics**: Visualisasi data training dan prediksi
- **Performance Metrics**: Monitoring akurasi dan performa model
- **Export Functionality**: Export hasil ke Excel/CSV
- **Historical Data**: Riwayat prediksi dan analisis

### 🎨 Antarmuka Modern
- **Responsive Design**: Optimal di desktop, tablet, dan mobile
- **Dark/Light Theme**: Tema yang dapat disesuaikan
- **Interactive Charts**: Grafik interaktif dengan Chart.js
- **Professional UI**: Design konsisten dengan komponen reusable

### 🔧 Fitur Teknis
- **RESTful API**: API dokumentasi lengkap dengan FastAPI
- **Real-time Validation**: Validasi input real-time di frontend
- **Error Handling**: Penanganan error yang komprehensif
- **Security**: JWT authentication dan input sanitization

---

## 🛠️ Teknologi

### Backend
- **Framework**: FastAPI 0.104+ (Python)
- **Machine Learning**: scikit-learn, NumPy, Pandas
- **Database**: MySQL 8.0+ dengan SQLAlchemy ORM
- **Authentication**: JWT dengan bcrypt hashing
- **API Documentation**: OpenAPI/Swagger UI
- **Server**: Uvicorn (development) / Gunicorn (production)

### Frontend
- **Framework**: React 18+ dengan Vite
- **Styling**: TailwindCSS 3.4+
- **Icons**: Lucide React
- **Charts**: Chart.js + React-Chart.js-2
- **HTTP Client**: Axios
- **Build Tool**: Vite untuk bundling modern

### DevOps & Tools
- **Version Control**: Git dengan GitHub
- **Environment**: Docker support (coming soon)
- **Testing**: Pytest (backend), Jest (frontend)
- **Code Quality**: ESLint, Prettier
- **Monitoring**: Custom logging dengan Loguru

---

## 📊 Performa Model

### 🎯 Metrik Evaluasi

| Metric | Score | Description |
|--------|-------|-------------|
| **Accuracy** | 93.7% | Akurasi keseluruhan model |
| **Precision** | 91.2% | Tingkat ketepatan prediksi positif |
| **Recall** | 89.8% | Tingkat deteksi alergen yang benar |
| **F1-Score** | 90.5% | Harmonic mean precision & recall |

### 🧪 Validasi Model
- **Cross-Validation**: K-Fold dengan K=10
- **Training Data**: 2000+ sampel produk makanan
- **Test Coverage**: 23 kategori alergen utama
- **Algorithm**: SVM + AdaBoost Ensemble

### 🍎 Alergen yang Didukung
```
Gandum • Susu • Telur • Kacang Tanah • Kedelai • Ikan • Udang • Kerang
Almond • Kenari • Mete • Wijen • Sulfites • MSG • Gluten • Laktosa
Casein • Whey • Tartrazine • Sodium Benzoate • dan lainnya...
```

---

## ⚙️ Instalasi

### 📋 Prasyarat Sistem

**Minimum Requirements:**
- **Python**: 3.10 atau lebih tinggi
- **Node.js**: 18.0 atau lebih tinggi  
- **npm/yarn**: Package manager
- **MySQL**: 8.0 atau lebih tinggi
- **Memory**: 4GB RAM minimum
- **Storage**: 2GB free space

### 🖥️ Windows Installation

#### 1. Install Python
```powershell
# Download Python dari https://python.org/downloads/
# Pastikan mencentang "Add Python to PATH"

# Verifikasi instalasi
python --version
pip --version
```

#### 2. Install Node.js
```powershell
# Download Node.js dari https://nodejs.org/
# Pilih LTS version (recommended)

# Verifikasi instalasi
node --version
npm --version
```

#### 3. Install MySQL
```powershell
# Download MySQL dari https://dev.mysql.com/downloads/installer/
# Install MySQL Community Server

# Atau menggunakan XAMPP/WAMP untuk development
```

#### 4. Clone Repository
```powershell
git clone https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN
```

#### 5. Setup Backend
```powershell
cd backend

# Buat virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_mysql.py

# Copy environment file
copy .env.example .env
# Edit .env sesuai konfigurasi Anda
```

#### 6. Setup Frontend
```powershell
cd ../frontend

# Install dependencies
npm install

# Atau menggunakan yarn
yarn install
```

### 🐧 Linux Installation

#### 1. Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# CentOS/RHEL/Fedora
sudo dnf install python3.10 python3-pip

# Verifikasi
python3 --version
pip3 --version
```

#### 2. Install Node.js
```bash
# Menggunakan NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Atau menggunakan nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Verifikasi
node --version
npm --version
```

#### 3. Install MySQL
```bash
# Ubuntu/Debian
sudo apt install mysql-server mysql-client

# CentOS/RHEL
sudo dnf install mysql-server mysql

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure installation
sudo mysql_secure_installation
```

#### 4. Clone & Setup Project
```bash
# Clone repository
git clone https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
python setup_mysql.py

# Environment configuration
cp .env.example .env
nano .env  # Edit configuration

# Setup frontend
cd ../frontend
npm install
```

### 🍎 macOS Installation

#### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Python
```bash
# Install Python using Homebrew
brew install python@3.10

# Verifikasi
python3 --version
pip3 --version
```

#### 3. Install Node.js
```bash
# Install Node.js using Homebrew
brew install node@18

# Atau menggunakan nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm install 18
nvm use 18

# Verifikasi
node --version
npm --version
```

#### 4. Install MySQL
```bash
# Install MySQL using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation
```

#### 5. Clone & Setup Project
```bash
# Clone repository
git clone https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
python setup_mysql.py

# Environment configuration
cp .env.example .env
vim .env  # Edit configuration

# Setup frontend
cd ../frontend
npm install
```

---

## 🚀 Menjalankan Aplikasi

### 🖥️ Development Mode

#### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

python run_dev.py
```
**Backend akan berjalan di**: http://localhost:8001  
**API Documentation**: http://localhost:8001/docs

#### 2. Start Frontend Server
```bash
# Terminal baru
cd frontend
npm run dev
```
**Frontend akan berjalan di**: http://localhost:5173

### 🏭 Production Mode

#### Backend Production
```bash
cd backend
source venv/bin/activate

# Menggunakan Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

#### Frontend Production
```bash
cd frontend

# Build untuk production
npm run build

# Preview build
npm run preview

# Atau deploy ke hosting (Vercel, Netlify, dll)
```

### 🐳 Docker Deployment (Coming Soon)
```bash
# Build dan run dengan Docker Compose
docker-compose up -d

# Atau manual build
docker build -t allerscan-backend ./backend
docker build -t allerscan-frontend ./frontend
```

---

## 📁 Struktur Proyek

```
SUPERBOOST-ALLERSCAN/
├── 📁 backend/                 # FastAPI Backend
│   ├── 📁 app/
│   │   ├── 📁 api/v1/         # API endpoints
│   │   ├── 📁 core/           # Core configurations
│   │   ├── 📁 database/       # Database configurations
│   │   ├── 📁 models/         # ML models & database models
│   │   ├── 📁 schemas/        # Pydantic schemas
│   │   ├── 📁 services/       # Business logic services
│   │   └── main.py           # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── run_dev.py           # Development server
│
├── 📁 frontend/               # React Frontend
│   ├── 📁 public/            # Static assets
│   ├── 📁 src/
│   │   ├── 📁 components/    # React components
│   │   ├── 📁 hooks/        # Custom React hooks
│   │   ├── 📁 services/     # API services
│   │   ├── 📁 styles/       # CSS styles
│   │   ├── 📁 utils/        # Utility functions
│   │   ├── App.jsx          # Main App component
│   │   └── main.jsx         # React entry point
│   ├── package.json         # Node.js dependencies
│   ├── tailwind.config.js   # TailwindCSS config
│   └── vite.config.js       # Vite configuration
│
├── 📁 data/                  # Dataset storage
│   └── 📁 raw/              # Raw datasets
│
├── 📁 notebooks/             # Jupyter notebooks
│   └── deteksi_alergen.ipynb # ML model development
│
├── 📁 scripts/               # Development & utility scripts
│   ├── 📁 debug/            # Debug scripts
│   ├── 📁 tests/            # Test scripts
│   └── 📁 logs/             # Script logs
│
├── 📁 docs/                  # Project documentation
│   ├── 📁 optimization/     # Optimization reports
│   ├── 📁 analysis/         # Analysis reports
│   └── PROJECT_STRUCTURE.md # Detailed structure guide
│
├── 📁 testing/               # Testing artifacts
│   └── 📁 exports/          # Test export files
│
├── 📁 logs/                  # Centralized logging
│   ├── 📁 backend/          # Backend logs
│   ├── 📁 frontend/         # Frontend logs
│   └── 📁 scripts/          # Script logs
│
├── README.md                # Project overview
├── .gitignore              # Git ignore rules
└── LICENSE                 # MIT License
```

> 📋 **Struktur Terbaru**: Proyek telah diorganisir ulang untuk pemisahan yang lebih baik antara development, production, dan documentation files. Lihat [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) untuk detail lengkap.

---

## 🔧 Konfigurasi

### ⚙️ Backend Configuration (.env)

```bash
# Application Settings
APP_NAME="AllerScan API"
APP_VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# API Configuration
API_V1_PREFIX="/api/v1"

# Database Configuration (MySQL)
DATABASE_URL="mysql+pymysql://user:password@localhost:3306/allerscan"

# CORS Settings
ALLOW_ORIGINS="http://localhost:3000,http://localhost:5173"

# ML Model Settings
CONFIDENCE_THRESHOLD=0.3
MAX_INPUT_LENGTH=1000

# Logging
LOG_LEVEL="INFO"
LOG_FILE="logs/allergen_api.log"
```

### 🎨 Frontend Configuration

**Vite Configuration (vite.config.js):**
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
```

**TailwindCSS Theme:**
```javascript
// Custom color palette
colors: {
  allerscan: {
    50: '#F0F9FF',
    500: '#0EA5E9',
    900: '#0C4A6E',
  }
}
```

---

## 📖 API Documentation

### 🔗 Endpoints Utama

#### Prediction Endpoints
```http
POST   /api/v1/predict              # Prediksi alergen
GET    /api/v1/predict/supported-allergens  # List alergen yang didukung
GET    /api/v1/predict/health       # Health check
```

#### Dataset Endpoints
```http
GET    /api/v1/dataset              # Get dataset dengan pagination
GET    /api/v1/dataset/stats        # Statistik dataset
GET    /api/v1/dataset/export/excel # Export ke Excel
DELETE /api/v1/dataset/predictions/{id}  # Hapus prediksi
```

### 📝 Request/Response Examples

#### Prediksi Alergen
```bash
curl -X POST "http://localhost:8001/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nama_produk_makanan": "Roti Tawar",
       "bahan_utama": "Tepung terigu, telur, susu",
       "pemanis": "Gula pasir",
       "lemak_minyak": "Mentega",
       "penyedap_rasa": "Garam, vanilla"
     }'
```

**Response:**
```json
{
  "success": true,
  "product_name": "Roti Tawar",
  "prediction": "Mengandung Alergen",
  "confidence_score": 0.87,
  "total_allergens_detected": 3,
  "detected_allergens": [
    {"allergen": "gandum", "confidence": 0.95},
    {"allergen": "telur", "confidence": 0.82},
    {"allergen": "susu", "confidence": 0.78}
  ],
  "processing_time": 245
}
```

### 📚 Interactive Documentation
Akses dokumentasi API interaktif di: http://localhost:8001/docs

### 📖 Additional Documentation

Dokumentasi lengkap proyek tersedia di folder `docs/`:

- **📊 Analysis Reports** (`docs/analysis/`)
  - Architecture Clean - Konsep arsitektur yang benar
  - Database Consolidation - Laporan konsolidasi database  
  - Documentation Cleanup - Laporan pembersihan dokumentasi
  - Final Status Working - Status fungsionalitas terkini
  - Frontend Errors Fixed - Laporan perbaikan frontend

- **🚀 Optimization Reports** (`docs/optimization/`)
  - Optimization Progress Fase 1-4 - Laporan optimisasi bertahap
  - Optimization Complete Fase 5-7 - Laporan optimisasi final

- **🏗️ Project Structure** (`docs/PROJECT_STRUCTURE.md`)
  - Panduan struktur proyek yang telah diorganisir
  - Benefits dan improvements yang telah dilakukan

---

## 🧪 Testing

### 🔍 Backend Testing
```bash
cd backend
source venv/bin/activate

# Unit tests
pytest tests/ -v

# Coverage report
pytest --cov=app tests/

# Test specific endpoint
python scripts/test_supported_allergens.py
```

### 🎨 Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Test dengan coverage
npm run test:coverage

# E2E testing (jika tersedia)
npm run test:e2e
```

### 🏥 Health Checks
```bash
# Backend health check
curl http://localhost:8001/api/v1/predict/health

# Database connectivity  
python scripts/verify_mysql.py

# Model validation
python scripts/test_confidence_fix.py

# Check database values
python scripts/check_db_values.py
```

### 📋 Available Test Scripts
```bash
# Script testing (located in scripts/)
python scripts/test_supported_allergens.py
python scripts/test_form_submission.py
python scripts/test_ingredient_parsing.py
python scripts/insert_samples_via_api.py
```

---

## 📈 Monitoring

### 📊 Metrics & Logging

**Centralized Logging Structure:**
- **Backend logs**: `logs/backend/allergen_api.log`
- **Frontend logs**: `logs/frontend/` (development)
- **Script logs**: `logs/scripts/` (utility scripts)

**Log Formats:**
- Backend: Structured JSON logging
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Performance Monitoring:**
```bash
# Response time monitoring  
tail -f logs/backend/allergen_api.log | grep "processing_time"

# Error rate monitoring
grep -c "ERROR" logs/backend/allergen_api.log

# Real-time log monitoring
tail -f logs/backend/allergen_api.log
```

### 🔔 Health Monitoring
```bash
# Database performance
python scripts/check_db_values.py

# Latest predictions check
python scripts/check_latest_predictions.py

# Database structure validation
python scripts/check_table_structure.py

# Model confidence testing  
python scripts/test_confidence_fix.py

# Form submission testing
python scripts/test_form_submission.py
```

### 📁 Monitoring Files Location
- **Scripts**: All monitoring scripts moved to `scripts/` folder
- **Logs**: Centralized in `logs/` with sub-categories
- **Testing**: Test artifacts in `testing/` folder

---

## 🤝 Kontribusi

Kami sangat menghargai kontribusi dari komunitas! Berikut cara berkontribusi:

### 🚀 Langkah Kontribusi

1. **Fork Repository**
   ```bash
   git clone https://github.com/your-username/SUPERBOOST-ALLERSCAN.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```

4. **Push & Pull Request**
   ```bash
   git push origin feature/amazing-feature
   # Buat Pull Request di GitHub
   ```

### 📋 Contribution Guidelines

- **Code Style**: Ikuti PEP 8 (Python) dan ESLint (JavaScript)
- **Testing**: Tambahkan tests untuk fitur baru
- **Documentation**: Update README dan docstrings
- **Commit Messages**: Gunakan conventional commits

### 🐛 Bug Reports
- Gunakan GitHub Issues
- Sertakan steps to reproduce
- Lampirkan screenshots jika perlu
- Berikan informasi environment

### 💡 Feature Requests
- Diskusikan di GitHub Discussions
- Jelaskan use case yang jelas
- Berikan mockup/wireframe jika ada

---

## 📄 Lisensi

Proyek ini dilisensikan under **MIT License**.

```
MIT License

Copyright (c) 2024 SuperBoost AllerScan Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Tim Pengembang

<div align="center">

### 🎓 **Universitas Nasional Karangturi**
*Fakultas Teknologi Informasi*

#### 👨‍💻 Core Team
- **Project Lead**: [Rynrd113](https://github.com/Rynrd113)
- **Machine Learning**: Tim Penelitian AI
- **Frontend Development**: React Development Team  
- **Backend Development**: FastAPI Development Team

#### 🏆 **Supported By**
- **BIMA DIKTI** - Badan Penelitian dan Pengembangan
- **DIKTISAINTEK BERDAMPAK** - Program Penelitian Terapan
- **Machine Learning Research Lab** - UNKAR

</div>

---

## 📞 Kontak & Support

<div align="center">

### 🌐 **Links**
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN)
[![Documentation](https://img.shields.io/badge/Docs-API%20Documentation-blue?logo=swagger)](http://localhost:8001/docs)
[![Demo](https://img.shields.io/badge/Demo-Live%20Preview-green?logo=vercel)](https://allerscan-demo.vercel.app)

### 📧 **Contact**
- **Email**: superboost.allerscan@unkar.ac.id
- **Website**: https://unkar.ac.id/research/allerscan
- **LinkedIn**: [SuperBoost AllerScan](https://linkedin.com/company/allerscan)

</div>

---

<div align="center">

### 🙏 **Acknowledgments**

Terima kasih kepada semua kontributor, penguji beta, dan komunitas open source  
yang telah mendukung pengembangan **SuperBoost AllerScan**.

### 📋 **Project Evolution**

Proyek ini telah melalui beberapa fase pengembangan dan optimisasi:
- **✅ Core Development**: Implementasi dasar dengan akurasi 93.7%
- **✅ Optimization Phases**: 7 fase optimisasi untuk performa dan UX  
- **✅ Restoration & Cleanup**: Stabilisasi ke versi core yang reliable
- **✅ Documentation Reorganization**: Struktur dokumentasi yang terorganisir

> 📂 **Dokumentasi Lengkap**: Semua riwayat pengembangan dan optimisasi tersedia di folder `docs/`

**© 2025 SuperBoost AllerScan • Machine Learning Research Project**

*"Menjadikan konsumsi makanan lebih aman melalui teknologi AI"*

---

⭐ **Jika proyek ini bermanfaat, berikan star di GitHub!** ⭐

</div>