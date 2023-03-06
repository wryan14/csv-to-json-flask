import os

# Flask app configuration
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')

# CSV to JSON converter configuration
CSV_DELIMITER = ','
JSON_INDENT = 2
