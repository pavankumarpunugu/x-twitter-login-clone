from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, LoginSession
from app.forms import ChangePasswordForm, UpdatePhoneForm
from app.routes import account_bp
from datetime import datetime

@account_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    sessions = LoginSession.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    return render_template('profile.html',
                         user=current_user,
                         sessions=sessions)


@account_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('account.change_password'))
        
        # Update password
        current_user.set_password(form.new_password.data)
        
        # Logout all other sessions
        LoginSession.query.filter(
            (LoginSession.user_id == current_user.id) &
            (LoginSession.token != request.headers.get('session_token', ''))
        ).update({'is_active': False})
        
        db.session.commit()
        
        flash('Password changed successfully. Please log in again on other devices.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('change_password.html', form=form)


@account_bp.route('/update-phone', methods=['GET', 'POST'])
@login_required
def update_phone():
    """Update phone number"""
    form = UpdatePhoneForm()
    
    if form.validate_on_submit():
        phone = form.phone.data.strip()
        
        # Check if phone already exists
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user and existing_user.id != current_user.id:
            flash('This phone number is already associated with another account.', 'danger')
            return redirect(url_for('account.update_phone'))
        
        current_user.phone = phone
        db.session.commit()
        
        flash('Phone number updated successfully.', 'success')
        return redirect(url_for('account.profile'))
    
    return render_template('update_phone.html', form=form)


@account_bp.route('/sessions')
@login_required
def sessions():
    """View active sessions"""
    sessions = LoginSession.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    return render_template('sessions.html', sessions=sessions)


@account_bp.route('/session/<int:session_id>/logout', methods=['POST'])
@login_required
def logout_session(session_id):
    """Logout specific session"""
    session = LoginSession.query.get(session_id)
    
    if not session or session.user_id != current_user.id:
        flash('Session not found.', 'danger')
        return redirect(url_for('account.sessions'))
    
    session.is_active = False
    db.session.commit()
    
    flash('Session logged out successfully.', 'success')
    return redirect(url_for('account.sessions'))


@account_bp.route('/logout-all-devices', methods=['POST'])
@login_required
def logout_all_devices():
    """Logout from all devices except current"""
    LoginSession.query.filter(
        (LoginSession.user_id == current_user.id) &
        (LoginSession.token != request.headers.get('session_token', ''))
    ).update({'is_active': False})
    
    db.session.commit()
    
    flash('Logged out from all other devices.', 'success')
    return redirect(url_for('main.dashboard'))


@account_bp.route('/settings')
@login_required
def settings():
    """Account settings page"""
    return render_template('settings.html', user=current_user)


@account_bp.route('/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate():
    """Deactivate account"""
    if request.method == 'POST':
        password = request.form.get('password')
        
        if not current_user.check_password(password):
            flash('Incorrect password.', 'danger')
            return redirect(url_for('account.deactivate'))
        
        current_user.is_active = False
        db.session.commit()
        
        from flask_login import logout_user
        logout_user()
        
        flash('Your account has been deactivated. You can reactivate it by logging in again.', 'info')
        return redirect(url_for('main.index'))
    
    return render_template('deactivate.html')


@account_bp.route('/download-data')
@login_required
def download_data():
    """Download user data"""
    import json
    from flask import send_file
    from io import BytesIO
    
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'phone': current_user.phone,
        'created_at': current_user.created_at.isoformat(),
        'email_confirmed': current_user.email_confirmed,
        'two_fa_enabled': current_user.two_fa_enabled,
        'backup_codes_count': current_user.get_backup_codes_count()
    }
    
    json_data = json.dumps(user_data, indent=2)
    bytes_io = BytesIO(json_data.encode())
    bytes_io.seek(0)
    
    return send_file(
        bytes_io,
        as_attachment=True,
        download_name=f'{current_user.username}_data.json',
        mimetype='application/json'
    )
