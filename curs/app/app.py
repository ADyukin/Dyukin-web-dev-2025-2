from flask import Flask
from flask_login import LoginManager
from .db import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Настройка кодировки для Flask
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
    
    # Инициализация расширений
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Регистрация blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .games import bp as games_bp
    app.register_blueprint(games_bp)
    
    return app 