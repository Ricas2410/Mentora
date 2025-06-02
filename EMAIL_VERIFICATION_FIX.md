# 🔧 Email Verification URL Fix for PythonAnywhere

## 🚨 Problem
Email verification links show `localhost:8000` instead of your PythonAnywhere domain, causing "site cannot be reached" errors.

## ✅ Solution

### Step 1: Update Your .env File on PythonAnywhere

Add these lines to your `.env` file on PythonAnywhere:

```env
# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
SITE_DOMAIN=yourusername.pythonanywhere.com
SITE_PROTOCOL=https
```

### Step 2: Run the Fix Script

In your PythonAnywhere console, navigate to your project directory and run:

```bash
cd /home/yourusername/Mentora
python scripts/fix_email_verification.py
```

### Step 3: Restart Your Web App

1. Go to your PythonAnywhere dashboard
2. Click on "Web" tab
3. Click the "Reload" button for your web app

### Step 4: Test Email Verification

1. Register a new test account with your real email
2. Check that the verification email contains your PythonAnywhere domain
3. Click the verification link to confirm it works

## 🔍 Alternative Method: Management Command

You can also use the Django management command:

```bash
python manage.py update_site_domain --domain yourusername.pythonanywhere.com --protocol https
```

## 📧 Example of Fixed Email

**Before (broken):**
```
http://localhost:8000/auth/verify-email/abc123.../
```

**After (working):**
```
https://yourusername.pythonanywhere.com/auth/verify-email/abc123.../
```

## 🛠️ Troubleshooting

### If the script doesn't work:

1. **Check your .env file location**: Make sure it's in the root directory of your project
2. **Verify environment variables**: Run `python manage.py shell` and check:
   ```python
   from django.conf import settings
   print(settings.SITE_DOMAIN)
   print(settings.SITE_PROTOCOL)
   ```
3. **Manual database update**: If needed, update directly:
   ```python
   from django.contrib.sites.models import Site
   site = Site.objects.get_current()
   site.domain = 'yourusername.pythonanywhere.com'
   site.save()
   ```

### If emails still show localhost:

1. Make sure you restarted your web app after updating .env
2. Check that your .env file is being loaded correctly
3. Verify the SITE_DOMAIN setting is correct

## ✅ Verification Checklist

- [ ] Updated .env file with correct SITE_DOMAIN and SITE_PROTOCOL
- [ ] Ran the fix script successfully
- [ ] Restarted the web application
- [ ] Tested with a new user registration
- [ ] Confirmed email contains correct domain
- [ ] Verified clicking the link works

## 🎯 Quick Fix Summary

```bash
# 1. Update .env file
echo "SITE_DOMAIN=yourusername.pythonanywhere.com" >> .env
echo "SITE_PROTOCOL=https" >> .env

# 2. Run fix script
python scripts/fix_email_verification.py

# 3. Restart web app (do this in PythonAnywhere dashboard)
```

That's it! Your email verification should now work correctly with your PythonAnywhere domain.
