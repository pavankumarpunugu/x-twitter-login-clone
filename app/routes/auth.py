from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, mail
from app.models import User, PasswordReset, LoginSession, LoginRequest
from app.forms import (
    LoginForm, RegistrationForm, ForgotPasswordForm,
    ResetPasswordForm, EmailVerificationForm, TwoFAVerificationForm
)
from app.routes import auth_bp
from datetime import datetime, timedelta
from flask_mail import Message
import secrets
import pyotp
import qrcode
from io import BytesIO
import base64

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate email confirmation token
        token = user.generate_confirmation_token()
        db.session.commit()
        
        # Send confirmation email
        send_confirmation_email(user, token)
        
        flash('Account created successfully! Please check your email to verify your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/confirm-email/<token>')
def confirm_email(token):
    """Confirm email via token"""
    if current_user.is_authenticated and current_user.email_confirmed:
        return redirect(url_for('main.dashboard'))
    
    user = User.query.filter_by(email_confirmation_token=token).first()
    if not user:
        flash('Invalid confirmation link.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.confirm_email(token):
        db.session.commit()
        flash('Email confirmed successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Confirmation link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        password = form.password.data
        
        # Find user by username, email, or phone
        user = User.query.filter(
            (User.username == identifier) |
            (User.email == identifier.lower()) |
            (User.phone == identifier)
        ).first()
        
        # Check if user exists and password is correct
        if not user:
            flash('Invalid username, email, or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check if account is locked
        if user.is_account_locked():
            flash('Account is temporarily locked due to multiple failed login attempts. Please try again later.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check email confirmation
        if not user.email_confirmed:
            flash('Please confirm your email before logging in.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verify password
        if not user.check_password(password):
            user.increment_failed_login()
            db.session.commit()
            flash('Invalid username, email, or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Password correct
        user.reset_failed_login()
        
        # Check if 2FA is enabled
        if user.two_fa_enabled:
            session['pre_2fa_user_id'] = user.id
            flash('2FA verification required.', 'info')
            return redirect(url_for('auth.verify_2fa'))
        
        # Check if new device/suspicious login
        if should_verify_login(user):
            login_request = LoginRequest(
                user_id=user.id,
                email=user.email,
                ip_address=get_client_ip(),
                user_agent=request.headers.get('User-Agent', ''),
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            token = secrets.token_urlsafe(32)
            login_request.token = token
            db.session.add(login_request)
            db.session.commit()
            
            send_login_confirmation_email(user, token)
            flash('A verification link has been sent to your email.', 'info')
            session['pending_user_id'] = user.id
            return redirect(url_for('auth.verify_login_request'))
        
        # Standard login
        user.last_login = datetime.utcnow()
        user.last_login_ip = get_client_ip()
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        login_session = LoginSession(
            user_id=user.id,
            token=session_token,
            user_agent=request.headers.get('User-Agent', ''),
            ip_address=get_client_ip(),
            device_name=get_device_name(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        db.session.add(login_session)
        db.session.commit()
        
        login_user(user, remember=form.remember_me.data)
        session['session_token'] = session_token
        
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html', form=form)


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """Verify 2FA during login"""
    if 'pre_2fa_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['pre_2fa_user_id'])
    if not user or not user.two_fa_enabled:
        return redirect(url_for('auth.login'))
    
    form = TwoFAVerificationForm()
    if form.validate_on_submit():
        code = form.code.data.strip()
        
        # Try TOTP verification
        if user.verify_totp(code):
            session.pop('pre_2fa_user_id', None)
            
            user.last_login = datetime.utcnow()
            user.last_login_ip = get_client_ip()
            db.session.commit()
            
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        
        # Try backup code
        if user.use_backup_code(code):
            session.pop('pre_2fa_user_id', None)
            
            user.last_login = datetime.utcnow()
            user.last_login_ip = get_client_ip()
            db.session.commit()
            
            login_user(user)
            flash('Successfully logged in! This backup code can no longer be used.', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid verification code.', 'danger')
    
    return render_template('verify_2fa.html', form=form, user=user)


@auth_bp.route('/verify-login-request', methods=['GET', 'POST'])
def verify_login_request():
    """Verify login request via email link"""
    token = request.args.get('token')
    
    if token:
        login_request = LoginRequest.query.filter_by(token=token).first()
        if not login_request or not login_request.is_valid():
            flash('Invalid or expired verification link.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_request.approve()
        db.session.commit()
        
        user = login_request.user
        user.last_login = datetime.utcnow()
        user.last_login_ip = login_request.ip_address
        db.session.commit()
        
        login_user(user)
        flash('Device verified! You are now logged in.', 'success')
        return redirect(url_for('main.dashboard'))
    
    if 'pending_user_id' in session:
        return render_template('verify_login_request.html')
    
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Initiate password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        
        user = User.query.filter(
            (User.username == identifier) |
            (User.email == identifier.lower()) |
            (User.phone == identifier)
        ).first()
        
        if user:
            # Generate password reset token
            token = secrets.token_urlsafe(32)
            password_reset = PasswordReset(
                user_id=user.id,
                token=token,
                email=user.email,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.session.add(password_reset)
            db.session.commit()
            
            # Send reset email
            send_password_reset_email(user, token)
            flash('Password reset link sent to your email.', 'info')
        else:
            flash('No account found with that information.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password via token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    password_reset = PasswordReset.query.filter_by(token=token).first()
    if not password_reset or not password_reset.is_valid():
        flash('Invalid or expired password reset link.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = password_reset.user
        user.set_password(form.password.data)
        user.reset_failed_login()
        
        password_reset.used = True
        password_reset.used_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Password reset successfully. Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form, token=token)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    # Delete session
    session_token = session.get('session_token')
    if session_token:
        login_session = LoginSession.query.filter_by(token=session_token).first()
        if login_session:
            db.session.delete(login_session)
            db.session.commit()
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


# Helper functions
def send_confirmation_email(user, token):
    """Send email confirmation link"""
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    msg = Message(
        subject='Confirm Your Email',
        recipients=[user.email],
        html=render_template('email/confirm_email.html',
                           user=user,
                           confirm_url=confirm_url)
    )
    mail.send(msg)


def send_password_reset_email(user, token):
    """Send password reset link"""
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg = Message(
        subject='Password Reset Request',
        recipients=[user.email],
        html=render_template('email/reset_password.html',
                           user=user,
                           reset_url=reset_url)
    )
    mail.send(msg)


def send_login_confirmation_email(user, token):
    """Send login verification link"""
    verify_url = url_for('auth.verify_login_request', token=token, _external=True)
    
    msg = Message(
        subject='Verify Your Login',
        recipients=[user.email],
        html=render_template('email/verify_login.html',
                           user=user,
                           verify_url=verify_url)
    )
    mail.send(msg)


def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


def get_device_name():
    """Get device name from user agent"""
    user_agent = request.headers.get('User-Agent', '')
    
    if 'Mobile' in user_agent:
        return 'Mobile Device'
    elif 'Tablet' in user_agent:
        return 'Tablet'
    else:
        return 'Desktop'


def should_verify_login(user):
    """Check if login verification is needed"""
    # Check if user has logged in before
    if not user.last_login:
        return False
    
    # Check if IP changed
    last_ip = user.last_login_ip
    current_ip = get_client_ip()
    
    if last_ip and last_ip != current_ip:
        return True
    
    return False
