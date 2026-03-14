# X - Twitter Clone

A full-stack Python Flask application replicating X (Twitter) login functionality with enterprise-grade security features.

## Features

### Authentication
- ✅ User Registration with email verification
- ✅ Secure Login with password hashing
- ✅ Password Reset via email
- ✅ Account recovery options
- ✅ Device fingerprinting

### Security
- ✅ Two-Factor Authentication (2FA) with TOTP
- ✅ Backup codes for account recovery
- ✅ Login attempt limiting and account lockout
- ✅ Session management and device tracking
- ✅ Password strength requirements
- ✅ CSRF protection
- ✅ Secure HTTP headers
- ✅ Login activity monitoring

### User Management
- ✅ Profile management
- ✅ Password change
- ✅ Phone number management
- ✅ Session management
- ✅ Account deactivation
- ✅ Data export

### Email Notifications
- ✅ Email confirmation
- ✅ Password reset emails
- ✅ Login verification emails
- ✅ Security alerts

## Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **2FA**: PyOTP (TOTP)
- **Email**: Flask-Mail
- **Forms**: WTForms
- **Security**: Werkzeug, CSRF Protection
- **Server**: Gunicorn
- **Deployment**: Railway.app, Heroku, or any WSGI-compatible platform

## Project Structure

```
x-twitter-login-clone/
├── app/
│   ├── __init__.py              # App factory
│   ├── models.py                # SQLAlchemy models
│   ├── forms.py                 # WTForms forms
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── account.py           # Account management routes
│   │   ├── security.py          # Security settings routes
│   │   └── main_routes.py       # Main routes
│   └── templates/
│       ├── base.html            # Base template
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── forgot_password.html
│       ├── reset_password.html
│       ├── security_overview.html
│       ├── two_fa_settings.html
│       ├── setup_2fa.html
│       ├── backup_codes.html
│       ├── profile.html
│       ├── change_password.html
│       ├── sessions.html
│       └── email/
│           ├── confirm_email.html
│           ├── reset_password.html
│           └── verify_login.html
├── config.py                    # Flask configuration
├── run.py                       # Application entry point
├── wsgi.py                      # WSGI entry point
├── requirements.txt             # Python dependencies
├── Procfile                     # Deployment configuration
├── .env.example                 # Environment variables template
└── .gitignore                   # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.8+
- pip or pip3
- PostgreSQL (for production) or SQLite (for development)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd x-twitter-login-clone
```

2. **Create and activate virtual environment**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Important environment variables for local development:**
```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///app.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

5. **Initialize database**
```bash
python run.py
```

6. **Run the application**
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Deployment on Railway.app

Railway is the recommended hosting platform for this application. Follow these steps:

### Step 1: Prepare Your GitHub Repository

1. **Initialize git repository (if not already done)**
```bash
git init
git add .
git commit -m "Initial commit: X Twitter Clone"
```

2. **Push to GitHub**
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### Step 2: Set Up Railway Project

1. **Go to Railway.app** and sign up/log in
   - Visit https://railway.app
   - Click "Start a New Project"

2. **Connect GitHub Repository**
   - Click "Deploy from GitHub"
   - Select your repository
   - Authorize Railway access to your GitHub account
   - Select the repository

3. **Add PostgreSQL Plugin**
   - In your Railway project, click "Add"
   - Select "PostgreSQL"
   - A new PostgreSQL database will be created
   - Railway automatically creates a `DATABASE_URL` variable

### Step 3: Configure Environment Variables

In your Railway project dashboard:

1. Click on your application service
2. Go to the "Variables" tab
3. Add the following environment variables:

```
SECRET_KEY=your-super-secret-key-generate-a-random-one
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@your-domain.com
```

**Important**: For Gmail SMTP:
- Use your Gmail address for `MAIL_USERNAME`
- Generate an App Password (not your Gmail password):
  1. Go to Google Account (myaccount.google.com)
  2. Select "Security" on the left
  3. Enable 2-Step Verification
  4. In "App passwords", select Mail and Windows Computer
  5. Copy the 16-character password and use it for `MAIL_PASSWORD`

### Step 4: Deploy

1. **Trigger deployment**
   - Railway automatically deploys when you push to main branch
   - Or click "Trigger Deploy" in Railway dashboard

2. **Monitor deployment**
   - Watch the build logs in Railway console
   - Wait for "Deployment Successful" message

3. **Access your application**
   - Railway provides a public URL
   - It will be in the format: `https://x-twitter-clone-xxxx.railway.app`

### Step 5: Verify Deployment

1. **Check application**
   - Visit your Railway app URL
   - Try registering a new account
   - Verify email functionality works

2. **Monitor logs**
   - Check Railway logs for any errors
   - Monitor application health

## Deployment on Heroku (Alternative)

If you prefer Heroku instead of Railway:

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-app-name
```

4. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=True
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
```

6. **Deploy**
```bash
git push heroku main
```

7. **Check logs**
```bash
heroku logs --tail
```

## Common Deployment Issues & Solutions

### Issue 1: Email not sending

**Problem**: Confirmation emails not being received

**Solutions**:
1. Verify Gmail App Password is correct
2. Check if 2FA is enabled on Gmail account
3. Verify `MAIL_USERNAME` and `MAIL_PASSWORD` are set correctly
4. Check application logs for SMTP errors
5. Try using a different email provider (SendGrid, Mailgun)

### Issue 2: Database connection error

**Problem**: `SQLALCHEMY_DATABASE_URI` not set or invalid

**Solutions**:
1. In Railway: Verify PostgreSQL plugin is added
2. Check `DATABASE_URL` variable is automatically created
3. If manually setting, use format: `postgresql://user:password@host:port/database`
4. Ensure database credentials are correct

### Issue 3: Secret key errors

**Problem**: Application won't start, "SECRET_KEY must be set"

**Solutions**:
1. Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```
2. Set `SECRET_KEY` environment variable in Railway
3. Ensure it's set for production environment

### Issue 4: Application crashes on deploy

**Problem**: Deployment fails during build/release

**Solutions**:
1. Check Railway logs for specific error
2. Verify all environment variables are set
3. Ensure `Procfile` is in root directory
4. Check `requirements.txt` for version conflicts
5. Try restarting deployment

### Issue 5: Password reset emails not working

**Problem**: Users receive password reset email but link doesn't work

**Solutions**:
1. Verify `MAIL_DEFAULT_SENDER` is set correctly
2. Check email links in logs
3. Ensure app URL is configured correctly
4. Verify email template paths are correct
5. Check email provider's spam folder

## First Time Setup Checklist

After deployment, complete these steps:

- [ ] Create a test user account
- [ ] Verify email confirmation works
- [ ] Test login functionality
- [ ] Enable 2FA on test account
- [ ] Test password reset
- [ ] Check login activity logs
- [ ] Verify all security features
- [ ] Test on mobile device
- [ ] Check responsiveness
- [ ] Monitor application logs

## Configuration & Customization

### Changing email provider

To use a different email provider (SendGrid, Mailgun, etc.):

1. Update `MAIL_SERVER` configuration
2. Set appropriate `MAIL_PORT`
3. Update `MAIL_USERNAME` and `MAIL_PASSWORD`
4. Test email functionality

Example for SendGrid:
```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

### Security recommendations

1. **Change SECRET_KEY regularly** for production
2. **Enable HTTPS** (Railway does this automatically)
3. **Use strong passwords** for database
4. **Monitor logs** for suspicious activity
5. **Update dependencies** regularly
6. **Enable 2FA** for admin accounts
7. **Set up automated backups** for database
8. **Review user sessions** periodically

## Development

### Running locally

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Run development server
python run.py
```

### Database migrations

The application uses SQLAlchemy ORM. Database tables are created automatically on first run.

To reset database during development:
```bash
rm app.db  # Delete SQLite database
python run.py  # Recreates tables
```

### Testing accounts

After setup, you can create test accounts:
1. Go to http://localhost:5000
2. Click "Sign Up"
3. Fill in credentials
4. Verify email by clicking link in console (or actual email if configured)

## Troubleshooting

### Database errors

- Verify PostgreSQL is running
- Check connection string is correct
- Ensure database exists and is accessible

### Authentication issues

- Clear browser cookies
- Check SECRET_KEY is set
- Verify email configuration
- Check user table exists in database

### 2FA issues

- Verify pyotp is installed
- Check device time is synchronized
- Try backup codes if authentication app fails
- Regenerate backup codes if needed

### Performance issues

- Check database query performance
- Monitor Railway resource usage
- Consider upgrading plan if needed
- Check application logs for errors

## Support & Documentation

- **Flask**: https://flask.palletsprojects.com
- **SQLAlchemy**: https://www.sqlalchemy.org
- **Railway Docs**: https://docs.railway.app
- **Heroku Docs**: https://devcenter.heroku.com

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Notes

This application includes enterprise-grade security features:

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Secure session management
- Two-factor authentication with PyOTP
- Login attempt limiting
- Password reset token validation
- Email verification
- Secure password requirements
- HttpOnly and Secure cookie flags
- SQL injection prevention via SQLAlchemy ORM

## Changelog

### Version 1.0.0 (Initial Release)
- User authentication system
- Email verification
- Password reset functionality
- Two-factor authentication
- Session management
- Security dashboard
- Account management
- Mobile-responsive design

---

**Made with ❤️ for secure authentication**

For issues, questions, or suggestions, please open an issue on GitHub.
