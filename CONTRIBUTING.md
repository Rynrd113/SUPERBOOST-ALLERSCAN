# Panduan Kontribusi

## Cara Berkontribusi

1. Fork repository ini
2. Buat branch untuk fitur baru (`git checkout -b feature/amazing-feature`)
3. Commit perubahan (`git commit -m 'Add some amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Setup database (XAMPP MySQL)
python ../scripts/setup_mysql.py
```

## Code Style

- **Python**: Ikuti PEP 8
- **JavaScript**: Gunakan ESLint dan Prettier
- **Commit Messages**: Gunakan conventional commits format

Untuk detail lengkap, lihat dokumentasi di folder `docs/`.
