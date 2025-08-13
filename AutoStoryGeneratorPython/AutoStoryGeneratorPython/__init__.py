"""
The flask application package.
"""

from flask import Flask
from .config.config import Config

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from .main.routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    return app

# To maintain compatibility with the existing runserver.py
app = create_app()
