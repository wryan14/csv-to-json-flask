import os
import sys
import unittest

import json
import io

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        test_data = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 35},
            {'name': 'Charlie', 'age': 30}
        ]

        # Save the test data to a file
        with open('data.json', 'w') as f:
            json.dump(test_data, f)

        # Create a test CSV file
        with open('test.csv', 'w') as f:
            f.write('Name,Age,Email\n')
            f.write('Alice,25,alice@example.com\n')
            f.write('Bob,30,bob@example.com\n')
        self.client = self.app.test_client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CSV to JSON Converter', response.data)

    def test_upload_file(self):
            # Test case where json_option is replace
            with open('test.csv', 'rb') as f:
                data = {'file': (f, 'test.csv'), 'json_option': 'replace'}
                response = self.client.post('/upload', data=data, content_type='multipart/form-data', buffered=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, b'{\n  "success": "Data saved successfully."\n}\n')

            # Test case where json_option is append and data.json exists
            existing_data = [{'name': 'John', 'age': 30}]
            with open('data.json', 'w') as f:
                json.dump(existing_data, f)
            csv_data = io.StringIO('name,age\nAlice,25\nBob,35\n')
            with open('test.csv', 'rb') as f:
                data = {'file': (f, 'test.csv'), 'json_option': 'append'}
                response = self.client.post('/upload', data=data, content_type='multipart/form-data', buffered=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, b'{\n  "success": "Data saved successfully."\n}\n')
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.assertEqual(len(data), 2)
                self.assertIn({'name': 'Alice', 'age': '25'}, data)
                self.assertIn({'name': 'Bob', 'age': '35'}, data)
            os.remove('data.json')

            # Test case where json_option is append and data.json does not exist
            csv_data = io.StringIO('name,age\nAlice,25\nBob,35\n')
            with open('test.csv', 'rb') as f:
                data = {'file': (f, 'test.csv'), 'json_option': 'append'}
                response = self.client.post('/upload', data=data, content_type='multipart/form-data', buffered=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, b'{\n  "success": "Data saved successfully."\n}\n')
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.assertEqual(len(data), 2)
                self.assertIn({'name': 'Alice', 'age': '25'}, data)
                self.assertIn({'name': 'Bob', 'age': '35'}, data)
            os.remove('data.json')
    

    def tearDown(self):
        # Remove the test CSV file
        os.remove('test.csv')
        os.remove('data.json')


if __name__ == '__main__':

    try:
        unittest.main()
    except SystemExit:
        pass
