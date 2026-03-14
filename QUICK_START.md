# QUICK START GUIDE - X TWITTER CLONE

## 30-Second Summary

This is a complete, production-ready X/Twitter login clone built with Flask and PostgreSQL. It includes:
- User registration & login
- Email verification
- 2FA with TOTP
- Password reset
- Session management
- Complete security features

## Files Included

```
x-twitter-login-clone/
├── app/                          # Main application code
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── forms.py                 # Form validation
│   ├── routes/                  # Route blueprints
│   │   ├── auth.py             # Login, signup, password reset
│   │   ├── account.py          # Profile, settings
│   │   ├── security.py         # 2FA, security settings
│   │   └── main_routes.py      # Homepage, dashboard
│   └── templates/              # HTML templates (25+ files)
│
├── config.py                    # Flask configuration
├── run.py                       # Application entry point
├── wsgi.py                      # Production WSGI
├── requirements.txt             # Python dependencies
├── Procfile                     # Deployment config
├── .env.example                 # Environment template
├── README.md                    # Full documentation
├── DEPLOYMENT_GUIDE.md         # Step-by-step Railway deployment
└── .gitignore                  # Git ignore rules
```

## Quick Start (Local)

### 1. Setup (2 minutes)
```bash
cd x-twitter-login-clone
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure .env
Edit `.env` with your settings:
```
FLASK_ENV=development
SECRET_KEY=dev-key
DATABASE_URL=sqlite:///app.db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 3. Run (1 minute)
```bash
python run.py
```

Visit: http://localhost:5000

### 4. Test
1. Click "Sign Up"
2. Create account with test email
3. Check console/logs for confirmation link
4. Click link to verify email
5. Login and explore features

## Deploy to Railway (5 minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "X Twitter Clone"
git push origin main
```

### 2. Create Railway Project
- Go to https://railway.app
- Click "New Project"
- Select "Deploy from GitHub"
- Choose your repository

### 3. Add Database
- Click "Add" in Railway
- Select PostgreSQL
- Done! (Railway configures DATABASE_URL automatically)

### 4. Set Environment Variables
In Railway dashboard, add:
```
SECRET_KEY=your-random-32-char-key
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. Deploy
- Railway auto-deploys on push
- Or click "Trigger Deploy"
- Wait 2-3 minutes
- Copy public URL and visit!

## Features Included

✅ **Authentication**
- Secure login/registration
- Email verification
- Password reset via email
- Account recovery

✅ **Security**
- Two-Factor Authentication (2FA)
- TOTP-based codes
- Backup codes
- Session tracking
- Login activity
- Account lockout on failed attempts

✅ **User Management**
- Profile settings
- Phone number management
- Password change
- Session management
- Account deactivation
- Data export

✅ **Email Integration**
- Confirmation emails
- Password reset emails
- Login verification emails
- Configurable SMTP

## Key Technologies

- **Backend**: Flask 2.3
- **Database**: PostgreSQL (production) / SQLite (dev)
- **Authentication**: Flask-Login
- **2FA**: PyOTP (TOTP)
- **Email**: Flask-Mail
- **ORM**: SQLAlchemy
- **Server**: Gunicorn
- **Deployment**: Railway, Heroku, AWS

## Important Files to Customize

### 1. Email Sender
**File**: `.env`
```
MAIL_DEFAULT_SENDER=your-domain@example.com
```

### 2. Application Name
**Files**: 
- `templates/base.html` (change 𝕏 logo)
- `config.py` (change app name in emails)

### 3. Security Settings
**File**: `config.py`
```python
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 30  # minutes
PASSWORD_RESET_TIMEOUT = 24  # hours
```

### 4. Database
**File**: `.env`
- Development: `sqlite:///app.db`
- Production: `postgresql://user:pass@host:port/db`

## Testing Accounts

During development, manually create accounts:
1. Register with test email
2. Check console output for confirmation link
3. Click link to verify
4. Login and explore

For 2FA testing:
1. Use Google Authenticator app (iOS/Android)
2. Scan QR code during 2FA setup
3. Enter 6-digit code to verify

## Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Ensure dependencies installed
pip install -r requirements.txt
```

### Issue: "Cannot connect to database"
```bash
# For dev, remove and recreate
rm app.db
python run.py
```

### Issue: Email not working
1. Check MAIL_USERNAME and MAIL_PASSWORD
2. For Gmail: Use 16-char App Password (not Gmail password)
3. Check spam folder
4. Review logs for SMTP errors

### Issue: 2FA QR code not scanning
1. Try manual entry of secret key
2. Ensure authenticator app is updated
3. Check phone time is correct
4. Use backup codes if available

## Configuration Files Explained

### config.py
- Development, testing, and production configurations
- Database settings
- Security defaults
- Session management

### run.py
- Application entry point
- Creates Flask app
- Sets up database
- Starts development server

### wsgi.py
- Production WSGI entry point
- Used by Gunicorn
- Environment configuration

### Procfile
- Deployment instructions
- Release phase (database setup)
- Web server command

### requirements.txt
- All Python dependencies
- Pinned to specific versions
- Can be updated safely

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| FLASK_ENV | Development/Production | development |
| SECRET_KEY | Session encryption key | random-32-char-string |
| DATABASE_URL | Database connection | postgresql://... |
| MAIL_SERVER | SMTP server | smtp.gmail.com |
| MAIL_PORT | SMTP port | 587 |
| MAIL_USERNAME | SMTP username | your-email@gmail.com |
| MAIL_PASSWORD | SMTP password | app-password-16-chars |
| MAIL_DEFAULT_SENDER | From address | noreply@example.com |
| PORT | Server port | 5000 |

## Git Workflow

```bash
# Make changes
nano app/routes/auth.py

# Test locally
python run.py

# Commit
git add .
git commit -m "Fix login bug"

# Push (triggers Railway deploy)
git push origin main
```

## Production Deployment Checklist

- [ ] Change SECRET_KEY to random 32+ char string
- [ ] Set FLASK_ENV=production
- [ ] Use PostgreSQL, not SQLite
- [ ] Configure MAIL variables
- [ ] Test email sending
- [ ] Test 2FA setup
- [ ] Test password reset
- [ ] Check all links work
- [ ] Monitor logs
- [ ] Set up backups
- [ ] Enable HTTPS (automatic on Railway)
- [ ] Review security settings

## Support Documents

**Full README**: See `README.md` for complete documentation

**Deployment Guide**: See `DEPLOYMENT_GUIDE.md` for detailed Railway setup

**API Reference**: Check `app/routes/` for endpoint documentation

## Next Steps

1. **Read DEPLOYMENT_GUIDE.md** for detailed Railway setup
2. **Customize branding** (logo, colors, app name)
3. **Configure email** with your SMTP provider
4. **Test thoroughly** before production
5. **Monitor logs** after deployment
6. **Set up backups** for database
7. **Plan updates** and maintenance

## Common Customizations

### Change logo/app name
Edit: `templates/base.html`

### Change colors
Edit: CSS in `templates/base.html` (`:root` section)

### Add custom authentication method
Edit: `app/routes/auth.py`

### Add new user fields
1. Update `app/models.py` (add column)
2. Update `app/forms.py` (add form field)
3. Update templates as needed

### Change email provider
Update `.env`:
- Gmail: smtp.gmail.com:587
- SendGrid: smtp.sendgrid.net:587
- Mailgun: smtp.mailgun.org:587

## Security Notes

✅ Already included:
- Password hashing (Werkzeug)
- CSRF protection
- Secure sessions
- SQL injection prevention
- 2FA support
- Login attempt limiting
- Email verification

⚠️ Add for production:
- Rate limiting (optional)
- API key authentication
- Log aggregation
- Intrusion detection
- Regular security audits

## Performance Tips

1. Use PostgreSQL (not SQLite)
2. Enable query caching
3. Optimize database indexes
4. Use CDN for static files
5. Upgrade Railway plan if needed

## License

This project is open source. Feel free to modify and deploy.

## Questions?

Check these in order:
1. README.md (comprehensive docs)
2. DEPLOYMENT_GUIDE.md (deployment specific)
3. Application logs (error details)
4. Source code comments

---

**You're all set! 🚀**

Start with: `python run.py`

Deploy with: `git push origin main`

Questions? Check the docs!
