from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()  # Initialize the db object

def create_app():
    app = Flask(__name__)  # Create the Flask app
    app.config.from_object(Config)  # Load configurations

    db.init_app(app)  # Initialize the db with the app

    # Register blueprints
    from app.routes.event_routes import bp as event_routes_bp
    from app.routes.auth_routes import bp as auth_routes_bp  # Import the auth blueprint

    app.register_blueprint(event_routes_bp)
    app.register_blueprint(auth_routes_bp)

    return app
