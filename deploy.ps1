# Pentora Platform Deployment Script for Fly.io (PowerShell)
# Optimized for free tier deployment

Write-Host "🚀 Starting Pentora Platform deployment to Fly.io..." -ForegroundColor Green

# Check if flyctl is installed
try {
    flyctl version | Out-Null
    Write-Host "✅ Fly.io CLI is ready" -ForegroundColor Green
} catch {
    Write-Host "❌ flyctl is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in to Fly.io
try {
    flyctl auth whoami | Out-Null
    Write-Host "✅ Logged in to Fly.io" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please log in to Fly.io first:" -ForegroundColor Yellow
    Write-Host "   flyctl auth login" -ForegroundColor Yellow
    exit 1
}

# Create app if it doesn't exist
Write-Host "📱 Creating Fly.io app (if not exists)..." -ForegroundColor Blue
try {
    flyctl apps create pentora 2>$null
    Write-Host "✅ App 'pentora' created successfully" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ App 'pentora' already exists or name taken, continuing..." -ForegroundColor Yellow
}

# Generate a secure secret key
Write-Host "🔐 Generating secure secret key..." -ForegroundColor Blue
$SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set secrets
Write-Host "🔐 Setting up secrets..." -ForegroundColor Blue
$secrets = @(
    "SECRET_KEY=$SECRET_KEY",
    "DEBUG=false",
    "DATABASE_URL=postgresql://neondb_owner:npg_CgOeQ9UVbzl3@ep-soft-mud-a234qcdh-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    "AWS_ACCESS_KEY_ID=c3478e6ba11e529c9c35764a68c25cd4",
    "AWS_SECRET_ACCESS_KEY=54f5d9b4a790d99ffea8f548a6471be072878287423b323c5966686df83538f0",
    "AWS_STORAGE_BUCKET_NAME=pentora-media-storage",
    "AWS_S3_REGION_NAME=us-east-1",
    "EMAIL_HOST_USER=info.pentora@gmail.com",
    "EMAIL_HOST_PASSWORD=clfu shzc xeqt nbqt",
    "SITE_NAME=Pentora",
    "ADMIN_EMAIL=admin@pentora.com"
)

foreach ($secret in $secrets) {
    flyctl secrets set $secret
}

Write-Host "✅ Secrets configured" -ForegroundColor Green

# Deploy the application
Write-Host "🚀 Deploying application..." -ForegroundColor Blue
flyctl deploy --ha=false --strategy immediate

# Check deployment status
Write-Host "🔍 Checking deployment status..." -ForegroundColor Blue
flyctl status

# Show app URL
try {
    $appInfo = flyctl info --json | ConvertFrom-Json
    $appUrl = "https://$($appInfo.Hostname)"
    Write-Host "🎉 Deployment complete!" -ForegroundColor Green
    Write-Host "📱 Your app is available at: $appUrl" -ForegroundColor Cyan
    Write-Host "🔧 Admin panel: $appUrl/my-admin/" -ForegroundColor Cyan
    Write-Host "📊 Analytics: $appUrl/analytics/dashboard/" -ForegroundColor Cyan
} catch {
    Write-Host "🎉 Deployment complete!" -ForegroundColor Green
    Write-Host "📱 Your app should be available at: https://pentora.fly.dev" -ForegroundColor Cyan
}

# Optional: Open the app in browser
$response = Read-Host "🌐 Open the app in your browser? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    flyctl open
}

Write-Host "✅ Deployment script completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Create a superuser: flyctl ssh console -C 'python manage.py createsuperuser'" -ForegroundColor White
Write-Host "   2. Check logs: flyctl logs" -ForegroundColor White
Write-Host "   3. Monitor app: flyctl dashboard" -ForegroundColor White
Write-Host ""
Write-Host "💡 Free tier tips:" -ForegroundColor Yellow
Write-Host "   - App will auto-sleep when inactive" -ForegroundColor White
Write-Host "   - First request after sleep may be slow" -ForegroundColor White
Write-Host "   - Monitor resource usage in Fly.io dashboard" -ForegroundColor White
