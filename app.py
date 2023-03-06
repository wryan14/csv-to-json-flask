from flask import Flask
from app import views

app = Flask(__name__)
app.register_blueprint(views)

# Load configuration settings from config.py
app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(debug=True)
