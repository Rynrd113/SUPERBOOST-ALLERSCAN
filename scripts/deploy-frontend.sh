#!/bin/bash
# Deploy script for AllerScan Frontend to GitHub Pages

echo "🚀 Deploying AllerScan Frontend to GitHub Pages..."

# Navigate to frontend directory
cd frontend

# Install dependencies if needed
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building project..."
npm run build

# Deploy to GitHub Pages
echo "🚀 Deploying to GitHub Pages..."
npm run deploy

echo "✅ Deployment complete!"
echo "📝 Your site should be available at: https://Rynrd113.github.io/SUPERBOOST-ALLERSCAN"
echo ""
echo "⏰ Note: It may take a few minutes for changes to appear."
echo "🔧 Don't forget to:"
echo "   1. Update the API URL in .env.production after deploying backend to Replit"
echo "   2. Rebuild and redeploy frontend after updating API URL"
