# CSV to JSON Converter

This Flask application converts CSV files to JSON data and exposes it through a REST API.

## Installation

1. Clone the repository: `git clone https://github.com/wryan14/csv-to-json-flask.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## Usage

1. Open the app in your web browser at http://localhost:5000
2. Select a CSV file to upload and convert
3. Click the "Convert to JSON" button to generate the JSON data
4. View data in a table at `/api-table`

## Search API

This API provides a search functionality for filtering JSON data based on keywords, fields, and keys.

### API Endpoint

`/api/search`

#### Parameters

- `q`: The search query (keyword) to filter the results (default: None).
- `field`: The field(s) to search in, separated by commas (default: None).
- `key`: The key to filter the results (default: None).

### Example Queries

1. Get all data without any filters:

`/api/search`


2. Filter data based on a keyword:

`/api/search?q=example`


3. Filter data based on a keyword in specific fields:

`/api/search?q=example&field=title,description`


4. Filter data based on a key:

`/api/search?key=example_key`


5. Filter data based on a keyword in specific fields and a key:

`/api/search?q=example&field=title,description&key=example_key`

#### Example

Suppose we have a JSON data file containing information about products, including their name, price, and category:

```
[
    {
        "name": "Product A",
        "price": 10.0,
        "category": "Category 1"
    },
    {
        "name": "Product B",
        "price": 20.0,
        "category": "Category 2"
    },
    {
        "name": "Product C",
        "price": 30.0,
        "category": "Category 1"
    },
    {
        "name": "Product D",
        "price": 40.0,
        "category": "Category 2"
    }
]
```

We can use the search API to filter this data based on various criteria. For example:

To get all products in category 1:
`/api/search?field=category&q=Category%201`

This will return the following JSON response:


```
[
    {
        "name": "Product A",
        "price": 10.0,
        "category": "Category 1"
    },
    {
        "name": "Product C",
        "price": 30.0,
        "category": "Category 1"
    }
]
```

To get all products with a price greater than 20:
`/api/search?q=20&field=price`

This will return the following JSON response:

```
[
    {
        "name": "Product C",
        "price": 30.0,
        "category": "Category 1"
    },
    {
        "name": "Product D",
        "price": 40.0,
        "category": "Category 2"
    }
]
```

To get the names and prices of all products in category 2:
`/api/search?key=name,price&field=category&q=Category%202`

This will return the following JSON response:

```
[
    {
        "name": "Product B",
        "price": 20.0
    },
    {
        "name": "Product D",
        "price": 40.0
    }
]
```

### Upload Endpoint

`/upload`

This endpoint handles file uploads and converts them to JSON. It returns a JSON response indicating success or failure. Use this to bypass the interface. 

#### Parameters
- `file`: The file to be uploaded. The file must be in CSV format.
- `json_option` (optional): The option for handling the JSON file. Valid options are `"replace"` (replace existing file with uploaded data) and `"append"` (append uploaded data to existing file). The default is `"replace"`.

```
import requests

url = "http://localhost:5000/upload"

payload = {}
files = [
  ('file', open('data.csv','rb'))
]
headers= {}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))
```

