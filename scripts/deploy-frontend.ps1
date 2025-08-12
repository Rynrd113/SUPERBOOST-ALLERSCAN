# Deploy script for AllerScan Frontend to GitHub Pages (PowerShell)

Write-Host "🚀 Deploying AllerScan Frontend to GitHub Pages..." -ForegroundColor Green

# Navigate to frontend directory
Set-Location "frontend"

# Install dependencies if needed
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

# Build the project
Write-Host "🔨 Building project..." -ForegroundColor Yellow
npm run build

# Deploy to GitHub Pages
Write-Host "🚀 Deploying to GitHub Pages..." -ForegroundColor Yellow
npm run deploy

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "📝 Your site should be available at: https://Rynrd113.github.io/SUPERBOOST-ALLERSCAN" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏰ Note: It may take a few minutes for changes to appear." -ForegroundColor Yellow
Write-Host "🔧 Don't forget to:" -ForegroundColor Yellow
Write-Host "   1. Update the API URL in .env.production after deploying backend to Replit" -ForegroundColor White
Write-Host "   2. Rebuild and redeploy frontend after updating API URL" -ForegroundColor White

# Return to root directory
Set-Location ".."
