"""View for main application"""
import json
import os
import glob
import requests
from flask import render_template, request, jsonify, current_app, url_for, redirect
from .helpers import read_csv
from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@views.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and convert to JSON.

    Returns:
        A JSON response indicating success or failure.
    """
    file = request.files['file']
    _, extension = os.path.splitext(file.filename)
    if extension != '.csv':
        return jsonify({'error': 'Invalid file type. The file must be a CSV.'}), 400
    try:
        data = read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        data = read_csv(file, encoding='cp1252')
    
    custom_filename = request.form.get('custom_filename', 'data.json')
    if not custom_filename.endswith('.json'):
        custom_filename += '.json'
        if custom_filename == '.json':
            custom_filename = 'data.json'
    
    filename = os.path.join(current_app.static_folder, custom_filename)

    with open(filename, 'w') as f:
        json.dump(data, f)

    return jsonify({'success': 'Data saved successfully.'}), 200


@views.route('/list_files', methods=['GET'])
def list_files():
    """Get the list of JSON files in the static folder.

    Returns:
        A JSON response containing the list of JSON files.
    """
    static_folder = current_app.static_folder
    json_files = glob.glob(os.path.join(static_folder, '*.json'))
    json_files = [os.path.basename(file) for file in json_files]

    return jsonify({'files': json_files}), 200

@views.route('/delete_file', methods=['POST'])
def delete_file():
    """Delete a JSON file from the static folder.

    Returns:
        A JSON response indicating success or failure.
    """
    filename = request.form.get('filename')
    if not filename:
        return jsonify({'error': 'Filename is missing.'}), 400

    file_path = os.path.join(current_app.static_folder, filename)
    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found.'}), 404

    os.remove(file_path)
    return jsonify({'success': 'File deleted successfully.'}), 200

@views.route('/file_manager', methods=['GET'])
def file_manager():
    """
    Render the file manager page, which allows users to view and delete JSON files
    in the Flask application's static folder.

    Returns:
        The rendered HTML for the file manager page.
    """
    return render_template('file_manager.html')


@views.route('/api/data/search')
@views.route('/api/data/<filename>/search')
def search(filename='data'):
    """
    Search API endpoint that returns results from a JSON data file.
    Args:
        filename (str): The filename of the JSON data file (default: 'data').
        q (str): The search query (keyword) to filter the results (default: None).
        field (str): The field(s) to search in, separated by commas. If not provided or empty string, all fields are searched (default: None).
        key (str): The key(s) to filter the results, separated by commas. If not provided or empty string, all items are returned (default: None).
    Returns:
        A JSON response containing search results or redirect to api-query-examples.html.html if the JSON data file does not exist or search results are empty.
    Raises:
        None
    """
    filename = f'{filename}.json'
    filepath = os.path.join(current_app.static_folder, filename)
    if not os.path.isfile(filepath):
        if not os.path.isfile(filename):
            response = requests.get(url_for('views.list_files', _external=True))
            response = response.json()['files']
            response = [x.split('.json')[0] for x in response]
            return render_template('api-query-examples.html', files=response)
        else:
            return render_template('api-query-examples.html', files=[filename.split('.json')[0]])

    with open(filepath) as f:
        data = json.load(f)

    search_query = request.args.get('q', '').strip().lower()
    fields = request.args.get('field', '').strip().split(',')
    key = request.args.get('key', '').strip()

    def match_field(item, search_query, fields):
        if search_query == '':
            return True

        if fields == ['']:
            # if no fields are specified, search all string fields
            for key, value in item.items():
                if isinstance(value, str) and search_query in value.lower():
                    return True
        else:
            # search only specified fields
            for field in fields:
                if field in item and isinstance(item[field], str) and search_query in item[field].lower():
                    return True

        return False

    if search_query == '' and fields == [''] and key == '':
        # Return entire data if no search parameters are provided
        results = data
    else:
        # Apply search filters if search parameters are provided
        results = []
        for item in data:
            if (fields==[''] or any(field in item for field in fields)) and match_field(item, search_query, fields):
                if key!='':
                    try:
                        results.append({k: item[k] for k in key.split(',')})
                    except KeyError:
                        print('Key Filter Error')
                else:
                    results.append(item)

    if not results:
        return jsonify({})

    return jsonify(results), 200, {'Content-Type': 'application/json'}


@views.route('/api-table')
def data_table():
    """
    Data table API endpoint that returns a list of columns and data from a JSON data file.

    Args:
        None

    Returns:
        A rendered HTML template containing a table of columns and data, or an error message.

    Raises:
        None
    """
    # Get the list of JSON files in the static folder
    json_files = os.listdir(current_app.static_folder)
    json_files = [file for file in json_files if file.endswith('.json')]

    if not json_files:
        return render_template('data-unavailable.html')

    # Set the filename to the first available JSON file
    filename_param = json_files[0]
    filename = os.path.join(current_app.static_folder, filename_param)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract column names from the JSON data
        columns = [{'data': key} for key in data[0].keys()]

        # Convert data to a list of lists for use in the template
        data_list = [list(row.values()) for row in data]
    except FileNotFoundError:
        error_msg = f'Error: could not find data file {filename_param}.'
        return render_template('api-table.html', error_msg=error_msg)

    # Get the list of JSON files in the static folder
    response = requests.get(url_for('views.list_files', _external=True))
    if response.status_code != 200:
        error_msg = 'Error: could not retrieve list of JSON files.'
        return render_template('api-table.html', error_msg=error_msg)
    json_files = response.json()['files']

    return render_template('api-table.html', columns=columns, data_list=data_list, json_files=json_files, filename=filename_param)


