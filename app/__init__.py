# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the db object here, but not yet the routes
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)  # Initialize db
    login_manager.init_app(app)  # Initialize login manager

    # Register blueprints here after initializing the app
    from app.routes.event_routes import bp as event_routes_bp
    from app.routes.auth_routes import bp as auth_routes_bp

    app.register_blueprint(event_routes_bp, url_prefix='/')
    app.register_blueprint(auth_routes_bp, url_prefix='/auth')

    # This line is important to handle the redirection for login_required
    login_manager.login_view = "auth.login"

    return app
