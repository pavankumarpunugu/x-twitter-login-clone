from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
account_bp = Blueprint('account', __name__, url_prefix='/account')
security_bp = Blueprint('security', __name__, url_prefix='/security')
main_bp = Blueprint('main', __name__)

# Import routes to register them
from app.routes import auth, account, security, main_routes
