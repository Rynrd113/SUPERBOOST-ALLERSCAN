# Panduan Instalasi Lengkap - SuperBoost AllerScan

## Prasyarat Sistem

**Minimum Requirements:**
- **Python**: 3.10 atau lebih tinggi
- **Node.js**: 18.0 atau lebih tinggi
- **npm/yarn**: Package manager
- **XAMPP**: Untuk MySQL server (recommended untuk development)
- **Memory**: 4GB RAM minimum
- **Storage**: 2GB free space

## Setup dengan XAMPP (Recommended untuk Development)

### 1. Install XAMPP
```bash
# Download XAMPP dari https://www.apachefriends.org/download.html
# Install XAMPP dengan komponen Apache dan MySQL
# Start Apache dan MySQL services dari XAMPP Control Panel
```

### 2. Install Python & Node.js
```bash
# Download Python dari https://python.org/downloads/
# Download Node.js dari https://nodejs.org/

# Verifikasi instalasi
python --version
node --version
npm --version
```

### 3. Clone Repository
```bash
git clone https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN
```

### 4. Setup Backend
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

# Setup database MySQL (pastikan XAMPP MySQL sudah berjalan)
python scripts/setup_mysql.py

# Konfigurasi environment (optional)
cp .env.example .env
nano .env  # Edit sesuai konfigurasi XAMPP Anda
```

### 5. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install
```

### 6. Konfigurasi Database (XAMPP)
- Buka XAMPP Control Panel
- Start **Apache** dan **MySQL** services
- Akses phpMyAdmin di http://localhost/phpmyadmin
- Database `allerscan_db` akan dibuat otomatis saat setup

## Instalasi Linux

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
sudo dnf update -y                      # CentOS/RHEL/Fedora
```

### 2. Install Python
```bash
# Ubuntu/Debian
sudo apt install python3.10 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install python3.10 python3-pip python3-venv

# Verifikasi
python3 --version
pip3 --version
```

### 3. Install Node.js
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL/Fedora
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install -y nodejs

# Atau menggunakan nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Verifikasi
node --version
npm --version
```

### 4. Install MySQL
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

### 5. Clone & Setup Project
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
python scripts/setup_mysql.py

# Environment configuration
cp .env.example .env
nano .env  # Edit configuration

# Setup frontend
cd ../frontend
npm install
```

## Instalasi macOS

### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python
```bash
# Install Python using Homebrew
brew install python@3.10

# Verifikasi
python3 --version
pip3 --version
```

### 3. Install Node.js
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

### 4. Install MySQL
```bash
# Install MySQL using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation
```

### 5. Clone & Setup Project
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
python scripts/setup_mysql.py

# Environment configuration
cp .env.example .env
vim .env  # Edit configuration

# Setup frontend
cd ../frontend
npm install
```

## Troubleshooting

### Python Issues
- **Python not found**: Pastikan Python 3.10+ terinstall dan ada di PATH
- **pip not found**: Install pip dengan `python -m ensurepip`
- **venv not found**: Install dengan `sudo apt install python3-venv`

### Node.js Issues
- **npm permission errors**: Gunakan nvm atau fix permissions
- **Node version conflicts**: Gunakan nvm untuk manage versions

### Database Issues
- **MySQL connection failed**: Pastikan XAMPP MySQL service berjalan
- **Access denied**: Check username/password di .env file
- **Port conflicts**: Ubah port MySQL di XAMPP configuration
