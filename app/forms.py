from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app.models import User
import re

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        Regexp('^[A-Za-z0-9_]+$', message='Username can only contain letters, numbers, and underscores')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=10, message='Password must be at least 10 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    agree_terms = BooleanField('I agree to the Terms of Service', validators=[
        DataRequired(message='You must agree to the terms')
    ])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_password(self, field):
        """Validate password strength"""
        password = field.data
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
            raise ValidationError('Password must contain at least one special character')


class LoginForm(FlaskForm):
    """User login form"""
    identifier = StringField('Username, Email, or Phone', validators=[
        DataRequired(message='Please enter your username, email, or phone number')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    
    remember_me = BooleanField('Remember me on this device')
    submit = SubmitField('Sign In')


class TwoFASetupForm(FlaskForm):
    """2FA setup form with TOTP verification"""
    totp_code = StringField('6-Digit Code', validators=[
        DataRequired(message='Code is required'),
        Length(min=6, max=6, message='Code must be 6 digits')
    ], render_kw={'placeholder': '000000', 'maxlength': '6'})
    
    submit = SubmitField('Verify & Enable 2FA')
    
    def validate_totp_code(self, field):
        """Ensure code is numeric"""
        if not field.data.isdigit():
            raise ValidationError('Code must contain only numbers')


class TwoFAVerificationForm(FlaskForm):
    """2FA verification during login"""
    method = StringField('2FA Method')
    
    # For TOTP/Backup code
    code = StringField('Code', render_kw={'placeholder': '000000'})
    
    # For SMS
    sms_code = StringField('SMS Code', render_kw={'placeholder': '000000'})
    
    submit = SubmitField('Verify')


class ForgotPasswordForm(FlaskForm):
    """Password recovery form"""
    identifier = StringField('Username, Email, or Phone', validators=[
        DataRequired(message='Please enter your username, email, or phone number')
    ])
    
    submit = SubmitField('Search Account')


class ResetPasswordForm(FlaskForm):
    """Password reset form"""
    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=10, message='Password must be at least 10 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Reset Password')
    
    def validate_password(self, field):
        """Validate password strength"""
        password = field.data
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
            raise ValidationError('Password must contain at least one special character')


class ChangePasswordForm(FlaskForm):
    """Change password form for authenticated users"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=10, message='Password must be at least 10 characters long')
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('new_password', message='Passwords must match')
    ])
    
    submit = SubmitField('Change Password')
    
    def validate_new_password(self, field):
        """Validate new password strength"""
        password = field.data
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
            raise ValidationError('Password must contain at least one special character')


class EmailVerificationForm(FlaskForm):
    """Email verification form"""
    submit = SubmitField('Verify Email')


class ResendConfirmationForm(FlaskForm):
    """Resend confirmation email form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    
    submit = SubmitField('Resend Confirmation Email')


class PhoneVerificationForm(FlaskForm):
    """Phone number verification form"""
    phone = StringField('Phone Number', validators=[
        DataRequired(message='Phone number is required'),
        Regexp(r'^\+?1?\d{9,15}$', message='Invalid phone number format')
    ], render_kw={'placeholder': '+1234567890'})
    
    code = StringField('Verification Code', validators=[
        Length(min=6, max=6, message='Code must be 6 digits')
    ], render_kw={'placeholder': '000000'})
    
    submit = SubmitField('Verify Phone')


class BackupCodeForm(FlaskForm):
    """Backup code entry form"""
    code = StringField('Backup Code', validators=[
        DataRequired(message='Backup code is required'),
        Length(min=8, max=8, message='Invalid backup code format')
    ], render_kw={'placeholder': 'XXXXXXXX'})
    
    submit = SubmitField('Use Backup Code')


class DisableTwoFAForm(FlaskForm):
    """Form to disable 2FA"""
    password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Password is required to disable 2FA')
    ])
    
    submit = SubmitField('Disable 2FA')


class UpdatePhoneForm(FlaskForm):
    """Update phone number form"""
    phone = StringField('Phone Number', validators=[
        DataRequired(message='Phone number is required'),
        Regexp(r'^\+?1?\d{9,15}$', message='Invalid phone number format')
    ], render_kw={'placeholder': '+1234567890'})
    
    submit = SubmitField('Update Phone Number')
