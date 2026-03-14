from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import string
import pyotp

class User(UserMixin, db.Model):
    """User model with authentication features"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Email verification
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_token = db.Column(db.String(100))
    email_confirmation_sent_at = db.Column(db.DateTime)
    
    # 2FA
    two_fa_enabled = db.Column(db.Boolean, default=False)
    totp_secret = db.Column(db.String(32))
    backup_codes = db.Column(db.Text)  # JSON string
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_locked = db.Column(db.Boolean, default=False)
    lock_until = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_changed_at = db.Column(db.DateTime)
    
    # Relationships
    sessions = db.relationship('LoginSession', backref='user', lazy=True, cascade='all, delete-orphan')
    password_resets = db.relationship('PasswordReset', backref='user', lazy=True, cascade='all, delete-orphan')
    login_requests = db.relationship('LoginRequest', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        self.password_changed_at = datetime.utcnow()
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self):
        """Generate email confirmation token"""
        token = secrets.token_urlsafe(32)
        self.email_confirmation_token = token
        self.email_confirmation_sent_at = datetime.utcnow()
        return token
    
    def confirm_email(self, token):
        """Verify email confirmation token"""
        if self.email_confirmation_token == token:
            if datetime.utcnow() - self.email_confirmation_sent_at < timedelta(hours=24):
                self.email_confirmed = True
                self.email_confirmation_token = None
                return True
        return False
    
    def setup_two_fa(self):
        """Generate TOTP secret for 2FA"""
        self.totp_secret = pyotp.random_base32()
        return self.totp_secret
    
    def verify_totp(self, token):
        """Verify TOTP token"""
        if self.totp_secret:
            totp = pyotp.TOTP(self.totp_secret)
            return totp.verify(token, valid_window=1)
        return False
    
    def get_totp_uri(self):
        """Get TOTP provisioning URI for QR code"""
        if self.totp_secret:
            totp = pyotp.TOTP(self.totp_secret)
            return totp.provisioning_uri(
                name=self.email,
                issuer_name='X-Twitter-Clone'
            )
        return None
    
    def generate_backup_codes(self, count=10):
        """Generate backup codes"""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            codes.append(code)
        
        self.backup_codes = ','.join(codes)
        return codes
    
    def use_backup_code(self, code):
        """Use a backup code (mark as used)"""
        if not self.backup_codes:
            return False
        
        codes = self.backup_codes.split(',')
        if code in codes:
            codes.remove(code)
            self.backup_codes = ','.join(codes)
            return True
        return False
    
    def has_backup_codes(self):
        """Check if user has unused backup codes"""
        if self.backup_codes:
            return len(self.backup_codes.split(',')) > 0
        return False
    
    def get_backup_codes_count(self):
        """Get count of unused backup codes"""
        if self.backup_codes:
            return len(self.backup_codes.split(','))
        return 0
    
    def is_account_locked(self):
        """Check if account is locked due to failed attempts"""
        if self.is_locked:
            if self.lock_until and datetime.utcnow() > self.lock_until:
                self.is_locked = False
                self.failed_login_attempts = 0
                return False
            return True
        return False
    
    def increment_failed_login(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.is_locked = True
            self.lock_until = datetime.utcnow() + timedelta(minutes=30)
    
    def reset_failed_login(self):
        """Reset failed login counter after successful login"""
        self.failed_login_attempts = 0
        self.is_locked = False
        self.lock_until = None
    
    def __repr__(self):
        return f'<User {self.username}>'


class LoginSession(db.Model):
    """Track user login sessions and devices"""
    __tablename__ = 'login_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_agent = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    device_name = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    is_active = db.Column(db.Boolean, default=True)
    
    def is_expired(self):
        """Check if session is expired"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False
    
    def __repr__(self):
        return f'<LoginSession {self.id}>'


class PasswordReset(db.Model):
    """Track password reset requests"""
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    
    def is_valid(self):
        """Check if reset token is valid and not expired"""
        if self.used:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def __repr__(self):
        return f'<PasswordReset {self.id}>'


class LoginRequest(db.Model):
    """Track login requests requiring approval"""
    __tablename__ = 'login_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    
    email = db.Column(db.String(120))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    device_name = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime)
    
    def is_valid(self):
        """Check if login request is still valid"""
        if self.approved:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def approve(self):
        """Approve login request"""
        self.approved = True
        self.approved_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<LoginRequest {self.id}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))
