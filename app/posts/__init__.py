from flask import Blueprint

post_bp = Blueprint('posts', __name__)
delete_bp = Blueprint('deletar',__name__)

from app.posts import routes

