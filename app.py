"""Main project application"""
from flask import Flask
from views import views

def create_app():
    """
    Creates a Flask application instance.

    Returns:
        Flask: The Flask application instance with registered blueprints and configuration settings loaded.
    """
    app = Flask(__name__)
    app.register_blueprint(views)
    # Load configuration settings from config.py
    app.config.from_pyfile('config.py')
    return app

if __name__ == '__main__':
    """
    Runs the Flask application in debug mode.
    """
    app = create_app()
    app.run(debug=True)
