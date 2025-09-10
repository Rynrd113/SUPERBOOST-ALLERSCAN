# 🚀 AllerScan Setup Guide untuk Mac dengan DBngin & TablePlus

Panduan lengkap menjalankan project AllerScan di macOS menggunakan DBngin dan TablePlus.

## 📋 Prerequisites yang Sudah Anda Miliki

✅ **DBngin** - Database manager untuk Mac  
✅ **TablePlus** - Database GUI client  
✅ **Python 3.9+** - Sudah terinstall  
✅ **Node.js 22.19.0** - Sudah terinstall  

## 🛠️ Setup Database

### 1. Pastikan DBngin Running
1. Buka **DBngin**
2. Pastikan **MySQL** service sedang running
3. Biasanya berjalan di `localhost:3306`

### 2. Buat Database
Buka **TablePlus** dan connect ke MySQL:
```
Host: localhost
Port: 3306
User: root
Password: (kosong)
```

Jalankan query untuk membuat database:
```sql
CREATE DATABASE allerscan_db;
```

## 🚀 Quick Start

### Opsi 1: Menggunakan Script Otomatis (Recommended)

```bash
cd /Users/mac/Desktop/SUPERBOOST-ALLERSCAN
./start_dev.sh
```

Script ini akan:
- ✅ Setup virtual environment Python
- ✅ Install semua dependencies
- ✅ Setup database dan tabel
- ✅ Start backend API (port 8001)
- ✅ Start frontend (port 3000)

### Opsi 2: Manual Setup

#### Setup Database
```bash
cd /Users/mac/Desktop/SUPERBOOST-ALLERSCAN
python3 setup_db_dbngin.py
```

#### Setup & Run Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_dev.py
```

#### Setup & Run Frontend (terminal baru)
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Akses Aplikasi

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React web application |
| **Backend API** | http://localhost:8001 | FastAPI REST API |
| **API Docs** | http://localhost:8001/docs | Interactive API documentation |

## 🗃️ Database Access dengan TablePlus

**Connection Settings:**
```
Host: localhost
Port: 3306
User: root  
Password: (kosong)
Database: allerscan_db
```

**Tables yang dibuat:**
- `allergen_results` - Hasil prediksi alergen
- `training_data` - Data training
- `dataset_results` - Hasil analisis dataset
- `form_test_results` - Hasil testing form
- `model_performance` - Performa model

## 🔧 Development Tools

### Cek Status Database
```bash
python3 db_check.py
```

### Stop All Services
```bash
# Jika menggunakan start_dev.sh
Ctrl + C

# Manual stop
lsof -ti:8001 | xargs kill -9  # Stop backend
lsof -ti:3000 | xargs kill -9  # Stop frontend
```

### Restart Services
```bash
./start_dev.sh
```

## 📊 Fitur Project

- **Machine Learning**: SVM + AdaBoost (93.7% accuracy)
- **Multi-allergen Detection**: 23+ jenis alergen
- **Real-time Prediction**: Analisis bahan makanan instant
- **Export Results**: Export ke Excel/CSV
- **Modern UI**: React + TailwindCSS
- **API Documentation**: FastAPI auto-generated docs

## 🐛 Troubleshooting

### MySQL Connection Error
```bash
# Cek apakah MySQL running
lsof -i :3306

# Restart DBngin MySQL service
# Buka DBngin → Stop MySQL → Start MySQL
```

### Port Already in Use
```bash
# Stop proses di port 8001 (backend)
lsof -ti:8001 | xargs kill -9

# Stop proses di port 3000 (frontend)  
lsof -ti:3000 | xargs kill -9
```

### Python Virtual Environment Issues
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node Modules Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📁 Project Structure

```
SUPERBOOST-ALLERSCAN/
├── backend/                 # FastAPI Backend
│   ├── app/                 # Application code  
│   ├── venv/                # Python virtual environment
│   ├── requirements.txt     # Python dependencies
│   └── run_dev.py          # Development server
├── frontend/               # React Frontend
│   ├── src/                # Source code
│   ├── node_modules/       # Node dependencies
│   └── package.json        # Node.js dependencies
├── data/raw/               # Dataset Excel
├── setup_db_dbngin.py     # Database setup script
├── db_check.py             # Database verification
├── start_dev.sh            # Development startup script
└── README_MAC.md           # This file
```

## 🎯 Next Steps

1. **Test API**: Buka http://localhost:8001/docs
2. **Test Frontend**: Buka http://localhost:3000
3. **View Database**: Gunakan TablePlus untuk melihat data
4. **Develop**: Mulai coding dengan hot-reload aktif

## 💡 Tips Development

- Backend auto-reload saat file berubah
- Frontend hot-reload dengan Vite
- Database changes bisa dilihat real-time di TablePlus
- Logs backend tersimpan di `backend/logs/allergen_api.log`

---

**Happy Coding! 🚀**
