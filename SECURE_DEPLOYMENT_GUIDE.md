# 🔒 Secure Email Configuration Guide

## ⚠️ SECURITY NOTICE
**NEVER commit email credentials to Git repositories!**

## 📧 Email Setup for Mentora Platform

### 🔧 Local Development Setup

1. **Create `.env.local` file** (this file is ignored by Git):
```bash
# Copy the template
cp .env .env.local
```

2. **Add your Gmail credentials to `.env.local`**:
```env
# Email Configuration - Real SMTP credentials
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=Mentora <your-email@gmail.com>
```

### 🔑 Gmail App Password Setup

1. **Enable 2-Factor Authentication**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → Enable

2. **Generate App Password**:
   - Security → App passwords
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter: **Mentora Platform**
   - Copy the 16-character password

3. **Update `.env.local`**:
   - Use your Gmail address as `EMAIL_HOST_USER`
   - Use the 16-character app password as `EMAIL_HOST_PASSWORD`

### 🌐 PythonAnywhere Deployment

1. **Upload your project** (without `.env.local`)

2. **Create `.env.local` on PythonAnywhere**:
```bash
# In your project directory on PythonAnywhere
nano .env.local
```

3. **Add the same email configuration**:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=Mentora <your-email@gmail.com>
```

4. **Restart your web app** from the PythonAnywhere dashboard

### 🧪 Testing Email System

1. **Test locally**:
```bash
python manage.py test_verification --email your-test-email@gmail.com
```

2. **Register a test account** and check your email

3. **Verify the email link works**

### 🔒 Security Best Practices

✅ **DO:**
- Use `.env.local` for sensitive credentials
- Use Gmail App Passwords (not regular passwords)
- Keep credentials out of Git repositories
- Use different credentials for development/production

❌ **DON'T:**
- Commit `.env.local` to Git
- Share credentials in chat/email
- Use your regular Gmail password
- Hardcode credentials in source code

### 📁 File Structure

```
Mentora/
├── .env                 # Template with placeholder values (committed)
├── .env.local          # Real credentials (NOT committed)
├── .gitignore          # Includes .env.local
└── mentora_platform/
    └── settings.py     # Loads from .env.local if exists
```

### 🔧 Environment Loading Logic

The settings.py automatically:
1. Checks if `.env.local` exists
2. If yes, loads from `.env.local` (with real credentials)
3. If no, loads from `.env` (with placeholder values)

### 🚨 Emergency: Credentials Compromised

If credentials are accidentally committed:

1. **Immediately change Gmail App Password**
2. **Remove from Git history**:
```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env.local' --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

3. **Generate new App Password**
4. **Update `.env.local` with new credentials**

### ✅ Verification Checklist

- [ ] `.env.local` exists and contains real credentials
- [ ] `.env.local` is in `.gitignore`
- [ ] `.env` contains only placeholder values
- [ ] Gmail 2FA is enabled
- [ ] App Password is generated and working
- [ ] Test email verification works
- [ ] No credentials in Git history

---

## 📞 Support

If you need help with email setup:
1. Check Gmail App Password setup
2. Verify `.env.local` file exists and has correct format
3. Test with the provided management command
4. Check Django logs for specific error messages
