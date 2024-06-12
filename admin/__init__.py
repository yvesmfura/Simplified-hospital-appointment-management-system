from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from .routes import *  # Explicitly import everything from routes