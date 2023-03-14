# Search API

This API provides a search functionality for filtering JSON data based on keywords, fields, and keys.

## API Endpoint

`/api/search`

### Parameters

- `q`: The search query (keyword) to filter the results (default: None).
- `field`: The field(s) to search in, separated by commas (default: None).
- `key`: The key to filter the results (default: None).

## Example Queries

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

