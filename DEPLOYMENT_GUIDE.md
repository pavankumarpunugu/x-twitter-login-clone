## DEPLOYMENT GUIDE - X TWITTER CLONE

### STEP-BY-STEP DEPLOYMENT ON RAILWAY.APP

---

## TABLE OF CONTENTS
1. Prerequisites
2. Local Setup
3. GitHub Setup
4. Railway Setup
5. Configuration
6. Testing
7. Troubleshooting

---

## SECTION 1: PREREQUISITES

### Required Accounts
- [x] GitHub account (free)
- [x] Gmail account (for email functionality)
- [x] Railway.app account (free tier available)

### Required Software (Already Installed)
- Python 3.8+
- Git
- pip

---

## SECTION 2: LOCAL SETUP (First Time Only)

### Step 2.1: Extract and Setup Project

```bash
# Navigate to project directory
cd x-twitter-login-clone

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2.2: Create .env File for Local Development

```bash
# Copy example
cp .env.example .env

# Edit .env file with your local settings
nano .env  # or use your preferred editor
```

**For local development, use these settings:**
```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=dev-secret-key-local-only
DATABASE_URL=sqlite:///app.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@example.com
PORT=5000
```

### Step 2.3: Run Locally

```bash
python run.py
```

Visit: http://localhost:5000

---

## SECTION 3: GITHUB SETUP

### Step 3.1: Initialize Git Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: X Twitter Clone application"
```

### Step 3.2: Create GitHub Repository

1. Go to https://github.com/new
2. Name: `x-twitter-login-clone`
3. Description: `X Twitter Clone - Full-stack Flask application with 2FA`
4. Make it PUBLIC (required for Railway free tier)
5. Click "Create repository"

### Step 3.3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/x-twitter-login-clone.git

# Rename branch
git branch -M main

# Push to GitHub
git push -u origin main
```

**If prompted for password:**
- Use GitHub Personal Access Token instead of password
- Create token at: https://github.com/settings/tokens
- Select: `repo` scope
- Copy token and paste when prompted

---

## SECTION 4: RAILWAY SETUP

### Step 4.1: Create Railway Project

1. Go to https://railway.app
2. Click "Start a New Project"
3. Click "Deploy from GitHub"
4. Authorize Railway to access your GitHub account
5. Select: `x-twitter-login-clone` repository
6. Click "Deploy"

### Step 4.2: Add PostgreSQL Database

**In Railway Dashboard:**

1. Click your project
2. Click "Add" (top right)
3. Select "PostgreSQL"
4. PostgreSQL will be added and configured automatically
5. Railway creates DATABASE_URL environment variable

**DO NOT modify database configuration - Railway handles it automatically**

### Step 4.3: Configure Environment Variables

**In Railway Dashboard:**

1. Click on your application service (usually named after repo)
2. Go to "Variables" tab
3. Add these variables:

```
SECRET_KEY=generate-a-secure-random-string-here
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@your-domain.com
```

**Important Security Note:**
- Never commit `.env` to GitHub
- Only set sensitive data in Railway dashboard
- The `.env` file is in `.gitignore` for security

---

## SECTION 5: GMAIL SETUP FOR EMAILS

### Step 5.1: Enable Gmail SMTP

1. Go to https://myaccount.google.com
2. Click "Security" (left sidebar)
3. Enable "2-Step Verification" if not already enabled
4. Scroll down to "App passwords"
5. Select: Mail → Windows Computer (or your platform)
6. Google generates a 16-character password
7. Copy this password (NOT your Gmail password)

### Step 5.2: Add to Railway

In Railway Variables, set:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

---

## SECTION 6: DEPLOYMENT

### Step 6.1: Trigger Deployment

**Option A: Automatic (Recommended)**
- Push to GitHub main branch
- Railway automatically deploys within 1-2 minutes

```bash
git add .
git commit -m "Update configuration"
git push origin main
```

**Option B: Manual**
- In Railway dashboard
- Click "Trigger Deploy" button

### Step 6.2: Monitor Deployment

1. In Railway dashboard, click your service
2. Go to "Deploy" tab
3. Watch build logs for:
   - ✅ "Collecting pip..." - Dependencies installing
   - ✅ "Successfully installed" - All packages installed
   - ✅ "Deployment Successful" - Ready to use
4. If you see errors, go to Section 7 (Troubleshooting)

### Step 6.3: Access Your Application

1. In Railway dashboard
2. Click your service
3. Copy the "Public URL"
4. Format: `https://x-twitter-clone-xxxx.railway.app`
5. Visit the URL in your browser

---

## SECTION 7: POST-DEPLOYMENT TESTING

### Test Checklist

Use this checklist to verify everything works:

- [ ] Homepage loads (/) 
- [ ] Sign Up page accessible
- [ ] Create test account
- [ ] Confirmation email sent and received
- [ ] Click confirmation link in email
- [ ] Email confirmed in app
- [ ] Login with test account works
- [ ] Dashboard loads after login
- [ ] 2FA setup works
- [ ] Can generate backup codes
- [ ] Can disable and re-enable 2FA
- [ ] Password change works
- [ ] Logout works
- [ ] Login activity visible
- [ ] Phone number update works
- [ ] Account deactivation works
- [ ] Privacy and Terms pages load

### Quick Test Steps

```
1. Visit https://your-app-name.railway.app
2. Click "Sign Up"
3. Enter:
   - Username: testuser123
   - Email: your-email@gmail.com
   - Password: TestPassword123!
4. Check email for confirmation
5. Click confirmation link
6. Login with credentials
7. Go to Security → 2FA
8. Enable 2FA and scan QR code
```

---

## SECTION 8: MONITORING & MAINTENANCE

### View Logs

**In Railway Dashboard:**
1. Click your service
2. Go to "Logs" tab
3. See all application events
4. Search for errors

### Common Log Messages
- `INFO:werkzeug:...GET /` → User visiting page (normal)
- `ERROR` or `Exception` → Something went wrong (check message)
- `SMTP Connection Error` → Email not working

### Update Code

1. Make changes locally
2. Test with `python run.py`
3. Commit: `git add . && git commit -m "message"`
4. Push: `git push origin main`
5. Railway auto-deploys (2-3 minutes)

### Database Backup

Railway PostgreSQL includes:
- Daily automated backups (30-day retention)
- Accessible from Railway dashboard
- Recovery available via support ticket

---

## SECTION 9: TROUBLESHOOTING

### Issue 1: Deployment fails with "Python not found"

**Solution:**
```bash
# Ensure Python 3.8+ is used
python3 --version
# Should show 3.8 or higher
```

### Issue 2: Emails not sending

**Symptoms:**
- Confirmation email not received
- No error in logs
- SMTP timeout

**Solutions:**
1. Verify Gmail App Password is correct (16 chars, no spaces)
2. Check "Less secure apps" is allowed in Gmail
3. Try alternative email provider (SendGrid, Mailgun)
4. Check spam/junk folder
5. Wait 5 minutes (Gmail SMTP can be slow)

**Alternative: Use SendGrid**
```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-sendgrid-key
```

### Issue 3: Database connection error

**Symptoms:**
- Application crashes on load
- "operationalError" in logs
- "Cannot connect to database"

**Solutions:**
1. Verify PostgreSQL plugin is added to Railway project
2. Check DATABASE_URL is set (should be automatic)
3. Restart Railway service: Click service → "Restart"
4. Verify database isn't at connection limit

### Issue 4: 500 Internal Server Error

**Solutions:**
1. Check application logs for specific error
2. Verify all environment variables are set
3. Check SECRET_KEY is long and random
4. Ensure requirements.txt has all dependencies
5. Restart service

**Quick fix:**
```bash
# Push a dummy change to trigger redeploy
git add .
git commit -m "Trigger redeploy" --allow-empty
git push origin main
```

### Issue 5: Page shows "Application Error"

**Causes:**
- Application crashed
- Database issue
- Missing environment variable

**Quick Diagnostics:**
1. Go to Railway Logs
2. Scroll to bottom
3. Look for error message
4. Search that error in troubleshooting section below

### Issue 6: 2FA not working

**Symptoms:**
- Can't scan QR code
- Code always shows as invalid

**Solutions:**
1. Ensure authenticator app is installed (Google Authenticator, Authy)
2. System time on phone must be accurate
3. Try manual entry of secret key instead of QR
4. Use backup code instead if available
5. Try different authenticator app

### Issue 7: "Dependency conflict" during deployment

**Symptoms:**
- Build fails with pip errors
- "No matching distribution" error

**Solution:**
Update requirements.txt - remove version pins:
```bash
# Old (specific version)
Flask==2.3.3

# New (compatible version)
Flask>=2.3
```

---

## SECTION 10: PRODUCTION CHECKLIST

Before going live, ensure:

- [ ] SECRET_KEY is strong (32+ characters, random)
- [ ] DATABASE_URL points to PostgreSQL (not SQLite)
- [ ] FLASK_ENV=production
- [ ] Email provider configured and working
- [ ] HTTPS enabled (Railway does this by default)
- [ ] Backup strategy in place
- [ ] Error logging configured
- [ ] Rate limiting implemented (if needed)
- [ ] CORS configured for any external APIs
- [ ] Session timeout set appropriately
- [ ] Passwords expire periodically (optional)
- [ ] Login attempts limited (already implemented)

---

## SECTION 11: PERFORMANCE OPTIMIZATION

### If experiencing slow loads:

1. **Check Railway logs** for slow queries
2. **Upgrade Railway plan** if at resource limits
3. **Add database indexing** if needed
4. **Enable caching** for static files
5. **Consider CDN** for static assets

### Current limitations (free tier):
- Up to 500MB RAM
- Limited execution time
- Shared database resources
- Single dyno/container

**Upgrade when:**
- App consistently slow
- Database > 100MB
- Need > 512MB RAM

---

## SECTION 12: SECURITY HARDENING

After deployment, implement:

1. **Change all test credentials**
2. **Enable 2FA on admin accounts**
3. **Review user data permissions**
4. **Monitor login attempts** daily
5. **Regular security audits**
6. **Update dependencies** monthly
7. **Review database backups**
8. **Enable security headers** (included)
9. **Implement rate limiting** (partially included)
10. **Monitor error logs** for attacks

---

## SECTION 13: USEFUL COMMANDS

### Local Development
```bash
# Start server
python run.py

# Database reset (development only)
rm app.db
python run.py

# Flask shell (for debugging)
flask shell

# Run tests (if implemented)
pytest
```

### Git/GitHub
```bash
# Check status
git status

# View changes
git diff

# Commit changes
git commit -am "message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main
```

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs

# Deploy
railway deploy
```

---

## SECTION 14: SUPPORT & RESOURCES

### Documentation
- Flask: https://flask.palletsprojects.com
- Railway: https://docs.railway.app
- PostgreSQL: https://www.postgresql.org/docs

### Common Issues
- Check application logs first
- Search Railway documentation
- Check GitHub issues
- Ask on Stack Overflow

### Report Issues
1. Describe the problem
2. Include error message
3. Include steps to reproduce
4. Include logs/screenshots
5. Mention deployment platform

---

## FINAL CHECKLIST

Before considering deployment complete:

- [ ] Application accessible via public URL
- [ ] Can create account
- [ ] Can verify email
- [ ] Can login
- [ ] Can enable 2FA
- [ ] Can view dashboard
- [ ] Can change password
- [ ] Can view login activity
- [ ] Email notifications working
- [ ] Password reset working
- [ ] No errors in logs
- [ ] Response time acceptable
- [ ] All links working
- [ ] Mobile responsive
- [ ] Security headers present

---

**Deployment Complete! 🎉**

Your X Twitter Clone is now live on Railway.app

For updates or modifications:
1. Make local changes
2. Test with `python run.py`
3. Commit to git
4. Push to GitHub
5. Railway auto-deploys

---

**Created: 2024**
**Last Updated: March 13, 2025**
**Version: 1.0.0**
