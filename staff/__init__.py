from flask import Blueprint

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

from .routes import *  # Explicitly import everything from routes
