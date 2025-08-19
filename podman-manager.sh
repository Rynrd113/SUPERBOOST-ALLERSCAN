#!/bin/bash

# 🚀 AllerScan Project Management Script
# Untuk menjalankan React + FastAPI dengan Podman (rootless)

set -e

PROJECT_ROOT="/home/ryn/Project/test/SUPERBOOST-ALLERSCAN"
NETWORK_NAME="allerscan-network"
BACKEND_CONTAINER="allerscan-backend"
FRONTEND_CONTAINER="allerscan-frontend"
MYSQL_CONTAINER="allerscan-mysql"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

echo_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to create network if it doesn't exist
create_network() {
    if ! podman network exists $NETWORK_NAME 2>/dev/null; then
        echo_info "Creating network: $NETWORK_NAME"
        podman network create $NETWORK_NAME
        echo_success "Network $NETWORK_NAME created"
    else
        echo_info "Network $NETWORK_NAME already exists"
    fi
}

# Function to build images
build_images() {
    echo_info "Building Docker images..."
    
    # Build backend image
    echo_info "Building backend image..."
    cd "$PROJECT_ROOT/backend"
    podman build -t allerscan-backend:dev .
    
    # Build frontend image
    echo_info "Building frontend image..."
    cd "$PROJECT_ROOT/frontend"
    podman build -t allerscan-frontend:dev .
    
    cd "$PROJECT_ROOT"
    echo_success "Images built successfully"
}

# Function to start services
start_services() {
    echo_info "Starting AllerScan services..."
    
    # Create network
    create_network
    
    # Stop and remove existing containers if they exist
    stop_services 2>/dev/null || true
    
    # Start MySQL first
    echo_info "Starting MySQL container..."
    podman run -d \
        --replace \
        --name $MYSQL_CONTAINER \
        --network $NETWORK_NAME \
        -p 3306:3306 \
        -e MYSQL_ROOT_PASSWORD=allerscan123 \
        -e MYSQL_DATABASE=allerscan_db \
        -e MYSQL_USER=allerscan \
        -e MYSQL_PASSWORD=allerscan123 \
        mysql:8.0
    
    # Wait for MySQL to be ready
    echo_info "Waiting for MySQL to be ready..."
    sleep 20
    
    # Start backend
    echo_info "Starting backend container..."
    podman run -d \
        --replace \
        --name $BACKEND_CONTAINER \
        --network $NETWORK_NAME \
        -p 8000:8000 \
        -e MYSQL_HOST=$MYSQL_CONTAINER \
        -e MYSQL_PORT=3306 \
        -e MYSQL_USER=allerscan \
        -e MYSQL_PASSWORD=allerscan123 \
        -e MYSQL_DATABASE=allerscan_db \
        -v "$PROJECT_ROOT/backend:/app:Z" \
        allerscan-backend:dev
    
    # Wait a moment for backend to start
    sleep 5
    
    # Start frontend
    echo_info "Starting frontend container..."
    podman run -d \
        --replace \
        --name $FRONTEND_CONTAINER \
        --network $NETWORK_NAME \
        -p 3000:3000 \
        -v "$PROJECT_ROOT/frontend:/app:Z" \
        -v "$PROJECT_ROOT/frontend/node_modules:/app/node_modules:Z" \
        allerscan-frontend:dev
    
    echo_success "Services started successfully!"
    echo_info "Frontend: http://localhost:3000"
    echo_info "Backend API: http://localhost:8000"
    echo_info "Backend Docs: http://localhost:8000/docs"
    echo_info "MySQL: localhost:3306 (user: allerscan, pass: allerscan123)"
}

# Function to stop services
stop_services() {
    echo_info "Stopping AllerScan services..."
    
    # Stop containers
    podman stop $FRONTEND_CONTAINER $BACKEND_CONTAINER $MYSQL_CONTAINER 2>/dev/null || true
    
    # Remove containers
    podman rm $FRONTEND_CONTAINER $BACKEND_CONTAINER $MYSQL_CONTAINER 2>/dev/null || true
    
    echo_success "Services stopped"
}

# Function to restart services
restart_services() {
    echo_info "Restarting AllerScan services..."
    stop_services
    sleep 2
    start_services
}

# Function to show logs
show_logs() {
    case $1 in
        "backend"|"be")
            echo_info "Showing backend logs..."
            podman logs -f $BACKEND_CONTAINER
            ;;
        "frontend"|"fe")
            echo_info "Showing frontend logs..."
            podman logs -f $FRONTEND_CONTAINER
            ;;
        "mysql"|"db")
            echo_info "Showing MySQL logs..."
            podman logs -f $MYSQL_CONTAINER
            ;;
        *)
            echo_info "Showing all logs..."
            echo_warning "MySQL logs:"
            podman logs --tail 10 $MYSQL_CONTAINER 2>/dev/null || echo "MySQL not running"
            echo_warning "Backend logs:"
            podman logs --tail 10 $BACKEND_CONTAINER 2>/dev/null || echo "Backend not running"
            echo_warning "Frontend logs:"
            podman logs --tail 10 $FRONTEND_CONTAINER 2>/dev/null || echo "Frontend not running"
            ;;
    esac
}

# Function to show status
show_status() {
    echo_info "AllerScan Project Status:"
    echo ""
    
    # Check if containers are running
    if podman ps --format "{{.Names}}" | grep -q $MYSQL_CONTAINER; then
        echo_success "MySQL: RUNNING (localhost:3306)"
    else
        echo_error "MySQL: STOPPED"
    fi
    
    if podman ps --format "{{.Names}}" | grep -q $BACKEND_CONTAINER; then
        echo_success "Backend: RUNNING (http://localhost:8000)"
    else
        echo_error "Backend: STOPPED"
    fi
    
    if podman ps --format "{{.Names}}" | grep -q $FRONTEND_CONTAINER; then
        echo_success "Frontend: RUNNING (http://localhost:3000)"
    else
        echo_error "Frontend: STOPPED"
    fi
    
    echo ""
    echo_info "Network: $NETWORK_NAME"
    podman network exists $NETWORK_NAME && echo_success "Network exists" || echo_error "Network not found"
}

# Function to clean up everything
cleanup() {
    echo_warning "Cleaning up AllerScan project..."
    
    # Stop services
    stop_services
    
    # Remove network
    if podman network exists $NETWORK_NAME 2>/dev/null; then
        podman network rm $NETWORK_NAME
        echo_success "Network $NETWORK_NAME removed"
    fi
    
    # Remove images (optional)
    read -p "Remove built images? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        podman rmi allerscan-backend:dev allerscan-frontend:dev 2>/dev/null || true
        echo_success "Images removed"
    fi
    
    echo_success "Cleanup complete"
}

# Main command handler
case $1 in
    "build")
        build_images
        ;;
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "logs")
        show_logs $2
        ;;
    "status")
        show_status
        ;;
    "cleanup")
        cleanup
        ;;
    *)
        echo -e "${BLUE}🚀 AllerScan Project Manager${NC}"
        echo ""
        echo "Usage: $0 {build|start|stop|restart|logs|status|cleanup}"
        echo ""
        echo "Commands:"
        echo "  build     - Build Docker images"
        echo "  start     - Start all services"
        echo "  stop      - Stop all services"
        echo "  restart   - Restart all services"
        echo "  logs      - Show logs (logs [backend|frontend|mysql])"
        echo "  status    - Show service status"
        echo "  cleanup   - Stop services and clean up"
        echo ""
        echo "Examples:"
        echo "  $0 build"
        echo "  $0 start"
        echo "  $0 logs backend"
        echo "  $0 status"
        ;;
esac
