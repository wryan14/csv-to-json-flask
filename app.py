from flask import Flask
from views import views

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    # Load configuration settings from config.py
    app.config.from_pyfile('config.py')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

