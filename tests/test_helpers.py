import os
import unittest
from app.helpers import read_csv

class TestHelpers(unittest.TestCase):
    def setUp(self):
        # Create a test CSV file
        with open('test.csv', 'w') as f:
            f.write('Name,Age,Email\n')
            f.write('Alice,25,alice@example.com\n')
            f.write('Bob,30,bob@example.com\n')

    def test_read_csv(self):
        data = read_csv('test.csv')
        expected_data = [
            {'Name': 'Alice', 'Age': '25', 'Email': 'alice@example.com'},
            {'Name': 'Bob', 'Age': '30', 'Email': 'bob@example.com'}
        ]
        self.assertEqual(data, expected_data)

    def tearDown(self):
        # Remove the test CSV file
        os.remove('test.csv')

if __name__ == '__main__':
    unittest.main()
