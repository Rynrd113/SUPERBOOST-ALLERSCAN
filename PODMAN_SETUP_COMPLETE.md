# 🚀 AllerScan Project - Podman Setup Complete

## ✅ Setup Status
Project **AllerScan** telah berhasil dikonfigurasi untuk berjalan dengan **Podman** di **Fedora 42**!

### 📋 Komponen yang Berjalan:
- **Frontend (React + Tailwind)**: http://localhost:3000
- **Backend (FastAPI)**: http://localhost:8000
- **Backend Documentation**: http://localhost:8000/docs
- **MySQL Database**: localhost:3306
  - Database: `allerscan_db`
  - User: `allerscan`
  - Password: `allerscan123`

---

## 🎯 Perintah Alias yang Tersedia

### 🔧 Management Commands:
```bash
proj-build      # Build Docker images
proj-start      # Start semua services (MySQL + Backend + Frontend)
proj-stop       # Stop semua services
proj-restart    # Restart semua services
proj-status     # Lihat status semua services
proj-logs       # Lihat logs semua services
proj-logs backend   # Lihat logs backend saja
proj-logs frontend  # Lihat logs frontend saja  
proj-logs mysql     # Lihat logs MySQL saja
proj-cleanup    # Bersihkan containers dan images
```

### 🗂️ Navigation Commands:
```bash
cdproj          # Go to project root
cdbe            # Go to backend folder
cdfe            # Go to frontend folder
```

### 🌐 Browser Commands:
```bash
open-frontend   # Buka frontend di Firefox
open-backend    # Buka backend docs di Firefox
```

---

## 🏃‍♂️ Quick Start Guide

### 1. **Start Project**:
```bash
proj-start
```

### 2. **Check Status**:
```bash
proj-status
```

### 3. **View Logs** (jika ada masalah):
```bash
proj-logs backend
```

### 4. **Access Application**:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### 5. **Stop Project**:
```bash
proj-stop
```

---

## 🔧 Technical Details

### **Container Architecture:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     MySQL       │
│  (React + Vite) │    │   (FastAPI)     │    │   (Database)    │
│                 │    │                 │    │                 │
│  Port: 3000     │────│  Port: 8000     │────│  Port: 3306     │
│                 │    │                 │    │                 │
│  Hot Reload: ✅ │    │  Hot Reload: ✅ │    │  Persistent: ✅ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ┌─────────────────┐
                    │  Podman Network │
                    │ allerscan-network │
                    └─────────────────┘
```

### **Volume Mounts:**
- **Frontend**: `/home/ryn/Project/test/SUPERBOOST-ALLERSCAN/frontend:/app:Z`
- **Backend**: `/home/ryn/Project/test/SUPERBOOST-ALLERSCAN/backend:/app:Z`
- **Node Modules**: Mounted untuk mencegah reinstall setiap build

### **Environment Variables:**
```bash
# Backend Environment
MYSQL_HOST=allerscan-mysql
MYSQL_PORT=3306
MYSQL_USER=allerscan
MYSQL_PASSWORD=allerscan123
MYSQL_DATABASE=allerscan_db
```

---

## 🐛 Troubleshooting

### **Services tidak start:**
```bash
proj-stop
proj-start
```

### **Port sudah digunakan:**
```bash
# Cek port yang digunakan
ss -tulpn | grep -E ':3000|:8000|:3306'

# Atau kill process yang menggunakan port
sudo kill -9 $(sudo lsof -t -i:3000)
```

### **Container error:**
```bash
# Lihat logs detail
proj-logs backend
proj-logs frontend
proj-logs mysql

# Clean up dan rebuild
proj-cleanup
proj-build
proj-start
```

### **Database connection error:**
```bash
# Pastikan MySQL sudah ready
proj-logs mysql

# Test koneksi database
podman exec -it allerscan-mysql mysql -u allerscan -pallerscan123 -e "SHOW DATABASES;"
```

---

## 📂 File Structure Created

```
SUPERBOOST-ALLERSCAN/
├── podman-manager.sh        # Main management script
├── setup-aliases.sh         # Alias setup script
├── backend/
│   ├── Dockerfile          # Backend container config
│   └── .dockerignore       # Backend ignore file
├── frontend/
│   ├── Dockerfile          # Frontend container config
│   └── .dockerignore       # Frontend ignore file
└── ~/.bashrc               # Updated with aliases
```

---

## 🎉 Success! 

Project **AllerScan** sekarang berjalan dengan **Podman** dan siap untuk development!

### **Testing URLs:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **API Health**: http://localhost:8000/api/v1/health
- 📚 **API Docs**: http://localhost:8000/docs
- 📊 **Database**: localhost:3306 (allerscan/allerscan123)

### **Hot Reload:**
- ✅ Frontend: Otomatis reload saat edit file React
- ✅ Backend: Otomatis reload saat edit file Python
- ✅ Database: Persistent data

**Happy Coding! 🎯**
