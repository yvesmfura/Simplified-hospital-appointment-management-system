from flask import Blueprint

client_bp = Blueprint('client', __name__, url_prefix='/client')

from .routes import *  # Explicitly import everything from routes