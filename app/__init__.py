from flask import Flask
from app.config import load_configurations, configure_logging
from .whatsapp.whatsapp import webhook_blueprint


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        app: The configured Flask application.
    """
    app = Flask(__name__)

    # Load configurations and logging settings
    load_configurations(app)
    configure_logging()

    # Import and register blueprints, if any
    app.register_blueprint(webhook_blueprint)

    return app
