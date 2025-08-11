# Panduan Development - SuperBoost AllerScan

## Development Mode

### Menjalankan Backend
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

python run_dev.py
```
**Backend berjalan di**: http://localhost:8001  
**API Documentation**: http://localhost:8001/docs

### Menjalankan Frontend  
```bash
cd frontend
npm run dev
```
**Frontend berjalan di**: http://localhost:5173

### XAMPP Development Setup

#### Start XAMPP Services
```bash
# Buka XAMPP Control Panel dan start:
# - Apache (port 80, 443)
# - MySQL (port 3306)
```

#### Database Management
- **phpMyAdmin**: http://localhost/phpmyadmin
- **Database Name**: allerscan_db
- **Default User**: root (no password untuk development)

## Production Mode

### Backend Production
```bash
cd backend
source venv/bin/activate

# Menggunakan Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

### Frontend Production
```bash
cd frontend

# Build untuk production
npm run build

# Preview build
npm run preview

# Deploy ke hosting (Vercel, Netlify, dll)
vercel --prod
```

## Testing & Development Tools

### Backend Testing
```bash
cd backend
source venv/bin/activate

# Unit tests
pytest tests/ -v

# Coverage report
pytest --cov=app tests/

# Test specific features
python scripts/test_supported_allergens.py
python scripts/test_form_submission.py
python scripts/test_ingredient_parsing.py
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Test dengan coverage
npm run test:coverage

# Linting
npm run lint

# Format code
npm run format
```

### Health Checks & Monitoring
```bash
# Backend health check
curl http://localhost:8001/api/v1/predict/health

# Database connectivity  
python scripts/check_db_values.py

# Model validation
python scripts/test_confidence_fix.py

# Latest predictions check
python scripts/check_newest_records.py

# Table structure validation
python scripts/check_table_structure.py
```

## Development Guidelines

### Code Style
- **Python**: Ikuti PEP 8, gunakan black formatter
- **JavaScript**: Ikuti ESLint rules, gunakan Prettier
- **Commit Messages**: Gunakan conventional commits format

### File Organization
- **Backend**: Ikuti Clean Architecture pattern
- **Frontend**: Component-based organization
- **Documentation**: Pisahkan docs berdasarkan kategori

### Database Development
- **Migrations**: Buat migration script untuk perubahan schema
- **Backup**: Backup database sebelum perubahan major
- **Testing Data**: Gunakan factory pattern untuk test data

### API Development
- **Documentation**: Update OpenAPI docs untuk endpoint baru
- **Versioning**: Gunakan API versioning (/api/v1/)
- **Testing**: Buat integration tests untuk endpoint baru

## Environment Variables

### Backend (.env)
```bash
# Application Settings
APP_NAME="AllerScan API"
APP_VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# API Configuration
API_V1_PREFIX="/api/v1"

# Database Configuration (XAMPP MySQL)
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD=""
MYSQL_DATABASE="allerscan_db"
DATABASE_URL="mysql+pymysql://root:@localhost:3306/allerscan_db"

# CORS Settings
ALLOW_ORIGINS="http://localhost:3000,http://localhost:5173"

# ML Model Settings
CONFIDENCE_THRESHOLD=0.3
MAX_INPUT_LENGTH=1000

# Logging
LOG_LEVEL="INFO"
LOG_FILE="logs/backend/allergen_api.log"
```

### Frontend Environment
```bash
# Vite environment variables
VITE_API_URL="http://localhost:8001"
VITE_APP_NAME="AllerScan"
VITE_ENVIRONMENT="development"
```

## Debugging

### Backend Debugging
```bash
# Enable debug logging
LOG_LEVEL="DEBUG" python run_dev.py

# Monitor logs
tail -f logs/backend/allergen_api.log

# Interactive debugging
python -m pdb scripts/debug_script.py
```

### Frontend Debugging
```bash
# Development tools
npm run dev

# Network debugging
# Open browser DevTools > Network tab

# Component debugging
# Install React Developer Tools extension
```

## Hot Reload & Development Experience

### Backend Hot Reload
```python
# run_dev.py sudah dikonfigurasi dengan reload
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend Hot Reload
```javascript
// vite.config.js otomatis enables HMR
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
  }
})
```

### Database Schema Changes
```bash
# Backup current database
mysqldump -u root allerscan_db > backup.sql

# Apply schema changes
python scripts/migrate_schema.py

# Test with development data
python scripts/insert_diverse_data.py
```
