import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from .db import db
from .auth import login_manager, bp as auth_bp
from .users import bp as users_bp
from .repositories import user_repository

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)

    from .cli import init_db_command
    app.cli.add_command(init_db_command)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.login_manager.init_app(app)

    from . import users
    app.register_blueprint(users.bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('users.index'))

    return app