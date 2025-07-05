#!/bin/bash

# Pentora Platform Deployment Script for Fly.io
# Optimized for free tier deployment

echo "🚀 Starting Pentora Platform deployment to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "   curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if user is logged in to Fly.io
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please log in to Fly.io first:"
    echo "   flyctl auth login"
    exit 1
fi

echo "✅ Fly.io CLI is ready"

# Create app if it doesn't exist
echo "📱 Creating Fly.io app (if not exists)..."
flyctl apps create pentora --generate-name || echo "App already exists"

# Set secrets
echo "🔐 Setting up secrets..."

# Generate a secure secret key if not provided
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
fi

flyctl secrets set \
    SECRET_KEY="$SECRET_KEY" \
    DEBUG="false" \
    DATABASE_URL="$DATABASE_URL" \
    AWS_ACCESS_KEY_ID="c3478e6ba11e529c9c35764a68c25cd4" \
    AWS_SECRET_ACCESS_KEY="54f5d9b4a790d99ffea8f548a6471be072878287423b323c5966686df83538f0" \
    AWS_STORAGE_BUCKET_NAME="pentora-media-storage" \
    AWS_S3_REGION_NAME="us-east-1" \
    EMAIL_HOST_USER="info.pentora@gmail.com" \
    EMAIL_HOST_PASSWORD="clfu shzc xeqt nbqt" \
    SITE_NAME="Pentora" \
    ADMIN_EMAIL="info.pentora.com"

echo "✅ Secrets configured"

# Deploy the application
echo "🚀 Deploying application..."
flyctl deploy --ha=false --strategy immediate

# Check deployment status
echo "🔍 Checking deployment status..."
flyctl status

# Show app URL
APP_URL=$(flyctl info --json | python -c "import sys, json; print('https://' + json.load(sys.stdin)['Hostname'])")
echo "🎉 Deployment complete!"
echo "📱 Your app is available at: $APP_URL"
echo "🔧 Admin panel: $APP_URL/my-admin/"
echo "📊 Analytics: $APP_URL/analytics/dashboard/"

# Optional: Open the app in browser
read -p "🌐 Open the app in your browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    flyctl open
fi

echo "✅ Deployment script completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Create a superuser: flyctl ssh console -C 'python manage.py createsuperuser'"
echo "   2. Check logs: flyctl logs"
echo "   3. Monitor app: flyctl dashboard"
echo ""
echo "💡 Free tier tips:"
echo "   - App will auto-sleep when inactive"
echo "   - First request after sleep may be slow"
echo "   - Monitor resource usage in Fly.io dashboard"
