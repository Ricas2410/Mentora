# 📧 Email Verification Setup Guide for Mentora

## 🔧 Current Status
Your Mentora platform is currently configured to print emails to the console (development mode). This means when users register, the verification email will appear in your terminal/console instead of being sent to their actual email address.

## 🚀 Quick Setup Options

### Option 1: Development Mode (Current - Console Emails)
**Best for:** Testing and development
**Current setting in .env:**
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**How it works:**
- When users register, they see: "Account created successfully! Check the console/terminal for your verification email (development mode)."
- The verification email appears in your terminal where you run `python manage.py runserver`
- You can copy the verification link from the console and test it

### Option 2: Production Mode (Real Emails via Gmail)
**Best for:** Live deployment on PythonAnywhere
**Required changes in .env:**

```env
# Change this line:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Add your Gmail credentials:
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

## 📋 Step-by-Step Gmail Setup (For Real Emails)

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under "Signing in to Google," click **2-Step Verification**
4. Follow the setup process if not already enabled

### Step 2: Generate App Password
1. In Google Account Settings → **Security**
2. Under "Signing in to Google," click **App passwords**
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Enter: **Mentora Platform**
6. Click **Generate**
7. **Copy the 16-character password** (you'll need this)

### Step 3: Update Your .env File
```env
# Email Configuration for Production
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop  # Your 16-character app password
DEFAULT_FROM_EMAIL=Mentora <noreply@mentora.com>
```

### Step 4: Test the Setup
1. Restart your Django server: `python manage.py runserver`
2. Create a test account with your real email address
3. Check your email inbox for the verification email

## 🌐 PythonAnywhere Deployment

### For PythonAnywhere:
1. Upload your updated `.env` file to your PythonAnywhere project directory
2. Make sure the `.env` file contains the Gmail settings above
3. Restart your web app from the PythonAnywhere dashboard
4. Test with a real email address

## 🔍 Testing Your Email Setup

### Test Script
Run this command to test your email configuration:
```bash
python scripts/setup_email_system.py
```

### Manual Test
1. Register a new account with your email address
2. Check the appropriate location for the verification email:
   - **Console mode:** Check your terminal/console output
   - **Gmail mode:** Check your email inbox (including spam folder)

## 🛠️ Troubleshooting

### Common Issues:

**1. "Authentication failed" error:**
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled on your Google account

**2. "SMTPAuthenticationError":**
- Double-check your EMAIL_HOST_USER (should be your full Gmail address)
- Verify your App Password is correct (16 characters with spaces)

**3. Emails going to spam:**
- This is normal for new sending domains
- Ask users to check their spam folder
- Consider using a professional email service for production

**4. "Connection refused" error:**
- Check your internet connection
- Verify EMAIL_HOST and EMAIL_PORT settings
- Make sure EMAIL_USE_TLS=True

### Debug Steps:
1. Check your `.env` file settings
2. Restart your Django server after making changes
3. Look at the console output for error messages
4. Test with the provided script: `python scripts/setup_email_system.py`

## 📝 Current Email Templates

Your platform includes professional email templates:
- **Text version:** `templates/emails/verification_email.txt`
- **HTML version:** `templates/emails/verification_email.html`

These templates include:
- Welcome message
- Clear verification instructions
- Professional branding
- 24-hour expiration notice

## 🔒 Security Notes

- **Never commit your .env file to Git** (it's already in .gitignore)
- **Use App Passwords, not your regular Gmail password**
- **Keep your email credentials secure**
- **Consider using a dedicated email account for your platform**

## 📞 Support

If you need help with email setup:
1. Check the troubleshooting section above
2. Run the test script to diagnose issues
3. Verify your Gmail App Password setup
4. Test with a simple email first before trying verification emails

---

**Current Status:** ✅ Email verification system is implemented and working
**Next Step:** Choose between console mode (development) or Gmail mode (production) based on your needs
