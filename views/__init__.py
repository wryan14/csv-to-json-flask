import json
import os
import pandas as pd
from flask import render_template, request, jsonify, current_app, redirect, url_for
from .helpers import read_csv
from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')

@views.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    data = read_csv(file)
    json_option = request.form.get('json_option', 'replace')
    filename = os.path.join(current_app.static_folder, 'data.json')
    if json_option == 'replace':
        with open(filename, 'w') as f:
            json.dump(data, f)
    elif json_option == 'append':
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
        combined_data = {}
        for dictionary in existing_data + data:
            combined_data.update(dictionary)
        with open(filename, 'w') as f:
            json.dump(combined_data, f)
    return 'Data saved successfully'

@views.route('/api/search')
def search():
    filename = os.path.join(current_app.static_folder, 'data.json')
    with open(filename) as f:
        data = json.load(f)
    search_query = request.args.get('q', '').strip()
    key = request.args.get('key', '').strip()
    results = []
    for item in data:
        if search_query:
            for k, v in item.items():
                if isinstance(v, str) and search_query.lower() in v.lower():
                    results.append(item)
                    break
        elif key:
            if key in item:
                results.append(item)
        else:
            results.append(item)
    return jsonify(results)

# Data Tables section
@views.route('/api-table')
def data_table():
    filename = os.path.join(current_app.static_folder, 'data.json')
    with open(filename, 'r') as f:
        data = json.load(f)
    # Extract column names from the JSON data
    columns = [{'data': key} for key in data[0].keys()]
    # Convert data to a list of lists for use in the template
    data_list = [list(row.values()) for row in data]
    return render_template('api-table.html', columns=columns, data_list=data_list)


