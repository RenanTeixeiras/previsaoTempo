from flask import Blueprint

get_bp = Blueprint('main', __name__)

from app.main import routes