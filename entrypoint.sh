#!/bin/bash
set -e

echo "🚀 Starting Pentora Platform deployment..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Deployment setup completed!"

# Start the application
echo "🌟 Starting Gunicorn server..."
exec gunicorn pentora_platform.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --threads 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level warning
