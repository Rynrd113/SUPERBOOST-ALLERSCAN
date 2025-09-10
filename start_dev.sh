#!/bin/bash
# 🚀 AllerScan Startup Script untuk Mac dengan DBngin & TablePlus
# Jalankan script ini untuk memulai development environment

echo "🚀 Starting AllerScan Development Environment"
echo "=============================================="

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function untuk print dengan warna
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "backend" ] && [ ! -d "frontend" ]; then
    print_error "Please run this script from the SUPERBOOST-ALLERSCAN root directory"
    exit 1
fi

print_info "Project directory: $(pwd)"

# Check if DBngin is running (check if MySQL port is active)
print_info "Checking if MySQL (DBngin) is running..."
if lsof -Pi :3306 -sTCP:LISTEN -t >/dev/null ; then
    print_status "MySQL is running on port 3306"
else
    print_warning "MySQL not detected on port 3306"
    print_info "Please make sure DBngin is running and MySQL service is started"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Setup Backend
print_info "Setting up Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
print_info "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Check database connection
print_info "Testing database connection..."
cd ..
python3 -c "
import pymysql
try:
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='allerscan_db')
    conn.close()
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('💡 Make sure DBngin MySQL is running and database exists')
"

# Start Backend in background
print_info "Starting Backend API..."
cd backend
source venv/bin/activate
python run_dev.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    print_status "Backend started successfully (PID: $BACKEND_PID)"
else
    print_error "Failed to start backend"
fi

# Setup Frontend
print_info "Setting up Frontend..."
cd frontend

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install
fi

# Start Frontend in background
print_info "Starting Frontend..."
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

# Check if frontend started successfully
if ps -p $FRONTEND_PID > /dev/null; then
    print_status "Frontend started successfully (PID: $FRONTEND_PID)"
else
    print_error "Failed to start frontend"
fi

# Print access information
echo ""
echo "🎉 AllerScan Development Environment Started!"
echo "=============================================="
print_info "Frontend: http://localhost:3000"
print_info "Backend API: http://localhost:8001"
print_info "API Documentation: http://localhost:8001/docs"
echo ""
print_info "Database Info for TablePlus:"
echo "  Host: localhost"
echo "  Port: 3306"
echo "  User: root"
echo "  Password: (empty)"
echo "  Database: allerscan_db"
echo ""
print_warning "Press Ctrl+C to stop all services"

# Function to cleanup when script is terminated
cleanup() {
    echo ""
    print_info "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    print_status "All services stopped"
    exit 0
}

# Set trap to cleanup on script termination
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
