from flask import Flask
import sys
sys.path.insert(0,'C:\\Users\\aluno\\Documents\\wwp')
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #extensions
    db.init_app(app)
    app.app_context().push()

    #blueprints
    from app.main import get_bp
    app.register_blueprint(get_bp)
    
    from app.posts import post_bp,delete_bp
    app.register_blueprint(post_bp)
    app.register_blueprint(delete_bp)


    return app

if __name__ ==  "__main__":
    create_app().run(debug=True)