#!/bin/bash
# 🚀 AllerScan Podman Deployment Script
# Untuk menjalankan AllerScan dengan Podman dan MySQL

set -e

echo "🚀 AllerScan - Podman Deployment"
echo "================================="

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fungsi untuk log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Start MySQL Container
log_info "Starting MySQL container..."
if podman ps -a | grep -q "mysql-allerscan"; then
    log_warning "MySQL container already exists, restarting..."
    podman stop mysql-allerscan || true
    podman rm mysql-allerscan || true
fi

podman run --name mysql-allerscan \
    -e MYSQL_ROOT_PASSWORD=root \
    -e MYSQL_DATABASE=allerscan_db \
    -p 3306:3306 \
    -d mysql:8.0

log_info "Waiting for MySQL to start..."
sleep 15

# 2. Verify MySQL connection
log_info "Creating database..."
podman exec mysql-allerscan mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS allerscan_db;" || log_warning "Database might already exist"

# 3. Start Backend
log_info "Starting AllerScan Backend..."
cd backend
/home/ryn/Project/test/SUPERBOOST-ALLERSCAN/backend/venv/bin/python run_dev.py &
BACKEND_PID=$!
cd ..

# 4. Start Frontend
log_info "Starting AllerScan Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

log_success "🎉 AllerScan deployed successfully!"
echo ""
log_info "📊 Services running:"
echo "   - MySQL:    http://localhost:3306"
echo "   - Backend:  http://localhost:8001"
echo "   - Frontend: http://localhost:3001"
echo "   - API Docs: http://localhost:8001/docs"
echo ""
log_info "🛑 To stop all services, run: pkill -f 'run_dev.py' && pkill -f 'npm run dev' && podman stop mysql-allerscan"
echo ""
log_warning "Press Ctrl+C to stop all services"

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID
