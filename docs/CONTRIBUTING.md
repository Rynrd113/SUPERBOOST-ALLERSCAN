# Panduan Kontribusi - SuperBoost AllerScan

## Selamat Datang Kontributor!

Kami menghargai kontribusi dari komunitas! Panduan ini akan membantu Anda berkontribusi pada proyek AllerScan.

## Langkah Kontribusi

### 1. Fork Repository
```bash
# Fork repository di GitHub, kemudian clone
git clone https://github.com/your-username/SUPERBOOST-ALLERSCAN.git
cd SUPERBOOST-ALLERSCAN

# Add upstream remote
git remote add upstream https://github.com/Rynrd113/SUPERBOOST-ALLERSCAN.git
```

### 2. Setup Development Environment
```bash
# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# Setup frontend  
cd ../frontend
npm install

# Setup database (XAMPP MySQL)
python scripts/setup_mysql.py
```

### 3. Create Feature Branch
```bash
# Sync dengan upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/amazing-feature
```

### 4. Develop & Test
```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd ../frontend  
npm test

# Manual testing
python scripts/test_form_submission.py
```

### 5. Commit Changes
```bash
# Stage changes
git add .

# Commit dengan conventional format
git commit -m "feat: add amazing feature"
```

### 6. Push & Pull Request
```bash
# Push feature branch
git push origin feature/amazing-feature

# Buat Pull Request di GitHub dengan template yang disediakan
```

## Contribution Guidelines

### Code Style

#### Python (Backend)
- **PEP 8**: Ikuti Python style guide
- **Black**: Gunakan black formatter
- **Type Hints**: Gunakan type hints untuk semua fungsi
- **Docstrings**: Google-style docstrings

```python
def predict_allergen(ingredients: str, confidence_threshold: float = 0.3) -> Dict[str, Any]:
    """
    Melakukan prediksi alergen berdasarkan bahan makanan.
    
    Args:
        ingredients: Daftar bahan makanan dalam string
        confidence_threshold: Threshold minimum untuk confidence score
        
    Returns:
        Dict berisi hasil prediksi dan metadata
        
    Raises:
        ModelError: Jika model tidak bisa melakukan prediksi
    """
    pass
```

#### JavaScript/React (Frontend)  
- **ESLint**: Ikuti ESLint rules yang sudah dikonfigurasi
- **Prettier**: Gunakan Prettier untuk formatting
- **JSDoc**: Dokumentasi untuk fungsi complex

```javascript
/**
 * Hook untuk mengelola state prediksi alergen
 * @param {Object} initialData - Data awal untuk form
 * @returns {Object} State dan handlers untuk prediksi
 */
const usePrediction = (initialData = {}) => {
  // Implementation
}
```

### Commit Message Format

Gunakan **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: Feature baru
- `fix`: Bug fix
- `docs`: Perubahan dokumentasi
- `style`: Formatting, whitespace, dll
- `refactor`: Code refactoring
- `test`: Menambah/memperbaiki tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(api): add allergen export functionality
fix(frontend): resolve pagination bug in dataset page  
docs(readme): update installation instructions
test(backend): add unit tests for prediction service
```

### Branch Naming

```bash
feature/feature-name       # Feature baru
bugfix/bug-description     # Bug fixes
hotfix/critical-fix        # Critical fixes
docs/documentation-update  # Documentation
refactor/code-cleanup      # Code refactoring
```

## Areas untuk Kontribusi

### 🧠 Machine Learning
- **Model Improvement**: Tingkatkan akurasi model
- **New Algorithms**: Implementasi algoritma ML baru
- **Feature Engineering**: Feature baru untuk training
- **Model Validation**: Cross-validation dan testing

### 🖥️ Backend Development
- **API Endpoints**: Endpoint baru atau improvement
- **Database**: Schema optimization, migrations
- **Performance**: Optimisasi query dan response time
- **Security**: Authentication, authorization, validation

### 🎨 Frontend Development  
- **UI Components**: Komponen reusable baru
- **User Experience**: Improvement pada UX/UI
- **Responsive Design**: Mobile optimization
- **Accessibility**: A11Y improvements

### 📚 Documentation
- **API Documentation**: OpenAPI/Swagger improvements
- **User Guides**: Tutorial dan panduan user
- **Code Comments**: Inline documentation
- **Architecture**: System design documentation

### 🧪 Testing
- **Unit Tests**: Backend dan frontend tests
- **Integration Tests**: API endpoint testing
- **E2E Tests**: End-to-end testing
- **Performance Tests**: Load testing dan benchmarking

## Pull Request Guidelines

### PR Template
Gunakan template berikut untuk PR:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process
1. **Automated Checks**: CI/CD pipeline must pass
2. **Code Review**: At least 1 reviewer approval  
3. **Testing**: Manual testing if needed
4. **Merge**: Squash and merge to main

## Issue Reporting

### Bug Reports
Gunakan template issue untuk bug reports:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Screenshots
Add screenshots if applicable

## Environment
- OS: [e.g. Windows 10, macOS, Ubuntu]
- Browser: [e.g. Chrome 91, Firefox 89]
- Python Version: [e.g. 3.10.0]
- Node.js Version: [e.g. 18.0.0]
```

### Feature Requests
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives
Alternative solutions considered

## Additional Context
Any other context or screenshots
```

## Development Setup

### Required Tools
- **Python**: 3.10+
- **Node.js**: 18.0+
- **XAMPP**: MySQL server
- **Git**: Version control
- **Code Editor**: VS Code (recommended)

### Recommended Extensions (VS Code)
- **Python**: Python extension pack
- **JavaScript**: ES7+ React/Redux/React-Native snippets
- **Formatting**: Prettier, Black Formatter
- **Git**: GitLens
- **Database**: MySQL extension

### Environment Variables
```bash
# Backend (.env)
ENVIRONMENT="development"
DEBUG=true
DATABASE_URL="mysql+pymysql://root:@localhost:3306/allerscan_db"
LOG_LEVEL="DEBUG"

# Frontend (.env.local)  
VITE_API_URL="http://localhost:8001"
VITE_ENVIRONMENT="development"
```

## Code Review Checklist

### For Reviewers
- [ ] Code follows project conventions
- [ ] Logic is clear and well-documented
- [ ] No obvious security issues
- [ ] Performance considerations addressed
- [ ] Tests cover new functionality
- [ ] Documentation updated if needed

### For Contributors
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log or debugging code
- [ ] Error handling implemented
- [ ] Code is readable and maintainable

## Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports dan feature requests
- **GitHub Discussions**: General questions dan ideas
- **Email**: Contact maintainers directly

### Resources
- **Documentation**: Folder `docs/`
- **API Reference**: http://localhost:8001/docs
- **Project Structure**: `docs/PROJECT_STRUCTURE.md`
- **Architecture**: `docs/analysis/ARCHITECTURE_CLEAN.md`

## Recognition

Contributors akan diakui dalam:
- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor graph dan stats

## Code of Conduct

### Expected Behavior
- Gunakan bahasa yang ramah dan inklusif
- Hormati pendapat dan pengalaman yang berbeda
- Berikan dan terima feedback yang konstruktif
- Focus pada yang terbaik untuk komunitas

### Unacceptable Behavior
- Harassment dalam bentuk apapun
- Trolling atau komentar yang menghina
- Public atau private harassment
- Publishing informasi pribadi tanpa izin

## License

Dengan berkontribusi, Anda setuju bahwa kontribusi Anda akan dilisensikan under MIT License yang sama dengan proyek ini.
