#!/bin/bash

# 🔧 Setup AllerScan Aliases for ~/.bashrc
# Script untuk menambahkan alias project ke bashrc

BASHRC_FILE="$HOME/.bashrc"
PROJECT_ROOT="/home/ryn/Project/test/SUPERBOOST-ALLERSCAN"
MANAGER_SCRIPT="$PROJECT_ROOT/podman-manager.sh"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Setting up AllerScan aliases...${NC}"

# Make manager script executable
chmod +x "$MANAGER_SCRIPT"

# Check if aliases already exist
if grep -q "# AllerScan Project Aliases" "$BASHRC_FILE" 2>/dev/null; then
    echo -e "${GREEN}✅ Aliases already exist in ~/.bashrc${NC}"
    exit 0
fi

# Add aliases to ~/.bashrc
cat >> "$BASHRC_FILE" << 'EOF'

# 🚀 AllerScan Project Aliases
# Added automatically by setup script

# Project management
alias proj-build='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh build'
alias proj-start='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh start'
alias proj-stop='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh stop'
alias proj-restart='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh restart'
alias proj-logs='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh logs'
alias proj-status='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh status'
alias proj-cleanup='bash /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/podman-manager.sh cleanup'

# Quick navigation
alias cdproj='cd /home/ryn/Project/test/SUPERBOOST-ALLERSCAN'
alias cdbe='cd /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/backend'
alias cdfe='cd /home/ryn/Project/test/SUPERBOOST-ALLERSCAN/frontend'

# Quick URLs
alias open-frontend='firefox http://localhost:3000 &'
alias open-backend='firefox http://localhost:8000/docs &'

EOF

echo -e "${GREEN}✅ Aliases added to ~/.bashrc${NC}"
echo ""
echo -e "${BLUE}📝 Available aliases:${NC}"
echo "  proj-build    - Build Docker images"
echo "  proj-start    - Start frontend + backend"
echo "  proj-stop     - Stop all services"
echo "  proj-restart  - Restart all services"
echo "  proj-logs     - Show logs"
echo "  proj-status   - Show service status"
echo "  proj-cleanup  - Clean up everything"
echo ""
echo "  cdproj        - Go to project root"
echo "  cdbe          - Go to backend folder"
echo "  cdfe          - Go to frontend folder"
echo ""
echo "  open-frontend - Open frontend in Firefox"
echo "  open-backend  - Open backend docs in Firefox"
echo ""
echo -e "${GREEN}🔄 Run 'source ~/.bashrc' or restart terminal to use aliases${NC}"
