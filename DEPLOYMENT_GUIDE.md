# 🚀 Pentora Platform Deployment Guide for Fly.io

## 📋 Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **Fly CLI**: Install flyctl
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```
3. **S3 Bucket**: Create `pentora-media-storage` bucket in AWS S3
4. **Database**: Neon PostgreSQL (already configured)

## 🔧 Pre-deployment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure S3 Bucket
- Create bucket: `pentora-media-storage`
- Region: `us-east-1`
- Set public read permissions for media files
- Configure CORS if needed

### 3. Test Locally with Production Settings
```bash
# Copy production environment
cp .env.production .env

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Test the application
python manage.py runserver
```

## 🚀 Deployment Steps

### 1. Login to Fly.io
```bash
flyctl auth login
```

### 2. Deploy Using Script (Recommended)
```bash
# Make script executable (Linux/macOS)
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

### 3. Manual Deployment (Alternative)

#### Create App
```bash
flyctl apps create pentora
```

#### Set Secrets
```bash
flyctl secrets set \
    SECRET_KEY="your-secret-key" \
    DEBUG="false" \
    DATABASE_URL="your-postgres-url" \
    AWS_ACCESS_KEY_ID="c3478e6ba11e529c9c35764a68c25cd4" \
    AWS_SECRET_ACCESS_KEY="54f5d9b4a790d99ffea8f548a6471be072878287423b323c5966686df83538f0" \
    EMAIL_HOST_PASSWORD="tdms ckdk tmgo fado"
```

#### Deploy
```bash
flyctl deploy --ha=false
```

## 🔍 Post-deployment

### 1. Create Superuser
```bash
flyctl ssh console -C "python manage.py createsuperuser"
```

### 2. Check Status
```bash
flyctl status
flyctl logs
```

### 3. Access Your App
- **Main Site**: https://pentora.fly.dev
- **Admin Panel**: https://pentora.fly.dev/my-admin/
- **Analytics**: https://pentora.fly.dev/analytics/dashboard/

## 💰 Free Tier Optimizations

### Resource Limits
- **CPU**: 1 shared CPU
- **Memory**: 256MB RAM
- **Storage**: 3GB volume
- **Bandwidth**: 160GB/month

### Optimizations Applied
- ✅ Auto-sleep when inactive
- ✅ Minimal worker processes (1 worker, 2 threads)
- ✅ Connection pooling
- ✅ Local memory caching
- ✅ Compressed static files
- ✅ Reduced logging
- ✅ S3 for media storage

### Monitoring Usage
```bash
# Check resource usage
flyctl dashboard

# Monitor logs
flyctl logs --follow

# Check app metrics
flyctl metrics
```

## 🛠️ Troubleshooting

### Common Issues

1. **App Won't Start**
   ```bash
   flyctl logs
   flyctl ssh console
   ```

2. **Database Connection Issues**
   - Verify DATABASE_URL secret
   - Check Neon database status

3. **Static Files Not Loading**
   ```bash
   flyctl ssh console -C "python manage.py collectstatic --noinput"
   ```

4. **S3 Media Issues**
   - Verify AWS credentials
   - Check bucket permissions
   - Test bucket access

### Performance Issues
- Monitor memory usage in Fly.io dashboard
- Check for memory leaks in logs
- Consider upgrading if consistently hitting limits

## 📊 Monitoring

### Built-in Monitoring
- **Health Checks**: Automatic health monitoring
- **Analytics Dashboard**: `/analytics/dashboard/`
- **Performance Tracking**: Disabled for free tier (can be enabled)

### External Monitoring
- Fly.io Dashboard: Resource usage
- Neon Dashboard: Database metrics
- AWS S3 Console: Storage usage

## 🔄 Updates and Maintenance

### Deploy Updates
```bash
git add .
git commit -m "Update description"
flyctl deploy
```

### Database Migrations
```bash
flyctl ssh console -C "python manage.py migrate"
```

### Backup Database
```bash
# Use Neon's built-in backup features
# Or export data manually
flyctl ssh console -C "python manage.py dumpdata > backup.json"
```

## 💡 Tips for Free Tier

1. **Monitor Usage**: Keep an eye on resource consumption
2. **Optimize Images**: Compress images before upload
3. **Cache Wisely**: Use local caching effectively
4. **Database Queries**: Optimize queries to reduce load
5. **Static Files**: Use S3 for large static assets
6. **Auto-sleep**: Let the app sleep when not in use

## 🆘 Support

- **Fly.io Docs**: https://fly.io/docs/
- **Django Docs**: https://docs.djangoproject.com/
- **AWS S3 Docs**: https://docs.aws.amazon.com/s3/

---

**🎉 Your Pentora Platform is now live on Fly.io with optimized free tier settings!**
