from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.routes import main_bp
from app.models import LoginSession
from datetime import datetime

@main_bp.route('/')
def index():
    """Homepage"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get recent login sessions
    sessions = LoginSession.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(LoginSession.last_active.desc()).limit(5).all()
    
    # Get account info
    days_since_password_change = None
    if current_user.password_changed_at:
        days_since_password_change = (datetime.utcnow() - current_user.password_changed_at).days
    
    return render_template('dashboard.html',
                         user=current_user,
                         sessions=sessions,
                         days_since_password_change=days_since_password_change)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/privacy')
def privacy():
    """Privacy policy"""
    return render_template('privacy.html')


@main_bp.route('/terms')
def terms():
    """Terms of service"""
    return render_template('terms.html')
