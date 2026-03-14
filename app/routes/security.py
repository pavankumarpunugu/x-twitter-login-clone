from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.forms import TwoFASetupForm, DisableTwoFAForm, BackupCodeForm
from app.routes import security_bp
from datetime import datetime
import pyotp
import qrcode
from io import BytesIO
import base64

@security_bp.route('/overview')
@login_required
def overview():
    """Security overview page"""
    return render_template('security_overview.html', user=current_user)


@security_bp.route('/two-fa')
@login_required
def two_fa():
    """2FA settings page"""
    return render_template('two_fa_settings.html', user=current_user)


@security_bp.route('/two-fa/setup', methods=['GET', 'POST'])
@login_required
def setup_two_fa():
    """Setup 2FA with TOTP"""
    # If already enabled, redirect
    if current_user.two_fa_enabled:
        flash('2FA is already enabled on your account.', 'info')
        return redirect(url_for('security.two_fa'))
    
    if request.method == 'GET':
        # Generate new TOTP secret
        secret = current_user.setup_two_fa()
        db.session.commit()
        
        # Generate QR code
        totp = pyotp.TOTP(secret)
        qr_uri = totp.provisioning_uri(
            name=current_user.email,
            issuer_name='X-Twitter-Clone'
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color='black', back_color='white')
        
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        qr_code_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        session['pending_2fa_secret'] = secret
        
        return render_template('setup_2fa.html',
                             user=current_user,
                             secret=secret,
                             qr_code=qr_code_base64,
                             backup_codes=None)
    
    # POST - Verify code
    form = TwoFASetupForm()
    if form.validate_on_submit():
        secret = session.get('pending_2fa_secret')
        if not secret:
            flash('Session expired. Please start again.', 'danger')
            return redirect(url_for('security.setup_two_fa'))
        
        totp = pyotp.TOTP(secret)
        if not totp.verify(form.totp_code.data, valid_window=1):
            flash('Invalid code. Please try again.', 'danger')
            return redirect(url_for('security.setup_two_fa'))
        
        # Enable 2FA
        current_user.totp_secret = secret
        current_user.two_fa_enabled = True
        
        # Generate backup codes
        backup_codes = current_user.generate_backup_codes(10)
        
        db.session.commit()
        session.pop('pending_2fa_secret', None)
        
        flash('2FA has been enabled successfully!', 'success')
        
        return render_template('backup_codes.html',
                             user=current_user,
                             backup_codes=backup_codes)
    
    return render_template('setup_2fa.html', form=form, user=current_user)


@security_bp.route('/two-fa/backup-codes')
@login_required
def backup_codes():
    """View and manage backup codes"""
    if not current_user.two_fa_enabled:
        flash('2FA is not enabled on your account.', 'info')
        return redirect(url_for('security.two_fa'))
    
    codes_count = current_user.get_backup_codes_count()
    
    return render_template('backup_codes_manage.html',
                         user=current_user,
                         codes_count=codes_count)


@security_bp.route('/two-fa/backup-codes/regenerate', methods=['POST'])
@login_required
def regenerate_backup_codes():
    """Regenerate backup codes"""
    if not current_user.two_fa_enabled:
        flash('2FA is not enabled on your account.', 'danger')
        return redirect(url_for('security.two_fa'))
    
    # Verify password
    password = request.form.get('password')
    if not current_user.check_password(password):
        flash('Incorrect password.', 'danger')
        return redirect(url_for('security.backup_codes'))
    
    # Generate new codes
    backup_codes = current_user.generate_backup_codes(10)
    db.session.commit()
    
    flash('Backup codes regenerated successfully.', 'success')
    
    return render_template('backup_codes.html',
                         user=current_user,
                         backup_codes=backup_codes)


@security_bp.route('/two-fa/disable', methods=['GET', 'POST'])
@login_required
def disable_two_fa():
    """Disable 2FA"""
    if not current_user.two_fa_enabled:
        flash('2FA is not enabled on your account.', 'info')
        return redirect(url_for('security.two_fa'))
    
    form = DisableTwoFAForm()
    if form.validate_on_submit():
        # Verify password
        if not current_user.check_password(form.password.data):
            flash('Incorrect password.', 'danger')
            return redirect(url_for('security.disable_two_fa'))
        
        # Disable 2FA
        current_user.two_fa_enabled = False
        current_user.totp_secret = None
        current_user.backup_codes = None
        
        db.session.commit()
        
        flash('2FA has been disabled successfully.', 'success')
        return redirect(url_for('security.two_fa'))
    
    return render_template('disable_two_fa.html', form=form, user=current_user)


@security_bp.route('/password')
@login_required
def password():
    """Password security page"""
    return render_template('password_security.html', user=current_user)


@security_bp.route('/login-activity')
@login_required
def login_activity():
    """View login activity and sessions"""
    from app.models import LoginSession
    
    sessions = LoginSession.query.filter_by(user_id=current_user.id).order_by(
        LoginSession.last_active.desc()
    ).all()
    
    return render_template('login_activity.html',
                         user=current_user,
                         sessions=sessions)


@security_bp.route('/trusted-devices')
@login_required
def trusted_devices():
    """Manage trusted devices"""
    from app.models import LoginSession
    
    sessions = LoginSession.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    return render_template('trusted_devices.html',
                         user=current_user,
                         sessions=sessions)


@security_bp.route('/remove-device/<int:session_id>', methods=['POST'])
@login_required
def remove_device(session_id):
    """Remove trusted device"""
    from app.models import LoginSession
    
    session_obj = LoginSession.query.get(session_id)
    
    if not session_obj or session_obj.user_id != current_user.id:
        flash('Device not found.', 'danger')
        return redirect(url_for('security.trusted_devices'))
    
    session_obj.is_active = False
    db.session.commit()
    
    flash('Device removed successfully.', 'success')
    return redirect(url_for('security.trusted_devices'))


@security_bp.route('/export-settings')
@login_required
def export_settings():
    """Export security settings"""
    from flask import send_file
    import json
    from io import BytesIO
    
    settings_data = {
        'user': current_user.username,
        'email_verified': current_user.email_confirmed,
        'two_fa_enabled': current_user.two_fa_enabled,
        'backup_codes_available': current_user.get_backup_codes_count(),
        'last_password_change': current_user.password_changed_at.isoformat() if current_user.password_changed_at else None,
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
        'created_at': current_user.created_at.isoformat(),
        'export_date': datetime.utcnow().isoformat()
    }
    
    json_data = json.dumps(settings_data, indent=2)
    bytes_io = BytesIO(json_data.encode())
    bytes_io.seek(0)
    
    return send_file(
        bytes_io,
        as_attachment=True,
        download_name=f'{current_user.username}_security_settings.json',
        mimetype='application/json'
    )


@security_bp.route('/api/check-2fa-status')
@login_required
def check_2fa_status():
    """API endpoint to check 2FA status"""
    return jsonify({
        'two_fa_enabled': current_user.two_fa_enabled,
        'backup_codes': current_user.get_backup_codes_count()
    })


@security_bp.route('/api/get-sessions')
@login_required
def get_sessions():
    """API endpoint to get active sessions"""
    from app.models import LoginSession
    
    sessions = LoginSession.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    sessions_data = [{
        'id': s.id,
        'device_name': s.device_name,
        'ip_address': s.ip_address,
        'last_active': s.last_active.isoformat(),
        'created_at': s.created_at.isoformat()
    } for s in sessions]
    
    return jsonify({'sessions': sessions_data})
