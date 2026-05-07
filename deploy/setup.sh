#!/bin/bash
# ============================================================
# Setup awal Hostinger VPS untuk SuperBoost AllerScan
# Jalankan sekali sebagai root atau dengan sudo
# ============================================================
set -e

REPO_URL="https://github.com/YOUR_USERNAME/YOUR_REPO.git"
APP_DIR="/var/www/superboost-allerscan"
DOMAIN="yourdomain.com"

echo "=== [1/7] Install system dependencies ==="
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip nodejs npm nginx git curl

echo "=== [2/7] Clone repository ==="
mkdir -p $APP_DIR
git clone $REPO_URL $APP_DIR
cd $APP_DIR

echo "=== [3/7] Setup backend ==="
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo ">>> Buat file .env dari template:"
cp .env.example .env
echo ">>> Edit /var/www/superboost-allerscan/backend/.env dengan kredensial database Anda!"
echo ">>> Tekan Enter setelah selesai mengedit..."
read -p ""

echo "=== [4/7] Build frontend ==="
cd $APP_DIR/frontend
npm ci
npm run build

echo "=== [5/7] Konfigurasi Nginx ==="
# Ganti yourdomain.com dengan domain asli
sed -i "s/yourdomain.com/$DOMAIN/g" $APP_DIR/deploy/nginx.conf
cp $APP_DIR/deploy/nginx.conf /etc/nginx/sites-available/allerscan
ln -sf /etc/nginx/sites-available/allerscan /etc/nginx/sites-enabled/allerscan
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "=== [6/7] Setup systemd service ==="
cp $APP_DIR/deploy/allerscan-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable allerscan-backend
systemctl start allerscan-backend

echo "=== [7/7] Setup SSH key untuk GitHub Actions ==="
echo ""
echo "Buat SSH key baru (tekan Enter untuk semua prompt):"
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions -N ""
echo ""
echo ">>> Tambahkan PUBLIC KEY berikut ke authorized_keys VPS:"
cat ~/.ssh/github_actions.pub
echo ""
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
echo ""
echo ">>> Tambahkan PRIVATE KEY berikut sebagai GitHub Secret SSH_PRIVATE_KEY:"
cat ~/.ssh/github_actions
echo ""
echo ">>> GitHub Secrets yang perlu dibuat:"
echo "    VPS_HOST     = IP VPS Hostinger Anda"
echo "    VPS_USER     = root (atau user Anda)"
echo "    SSH_PRIVATE_KEY = (isi dengan private key di atas)"
echo ""
echo "=== Setup selesai! ==="
echo "Backend: sudo systemctl status allerscan-backend"
echo "Nginx:   sudo systemctl status nginx"
