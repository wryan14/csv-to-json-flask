import csv
from io import TextIOWrapper

import csv
from io import TextIOWrapper

def read_csv(file, encoding='utf-8'):
    """
    Reads a CSV file and returns the data as a list of dictionaries.

    Args:
        file (file): The CSV file to read.
        encoding (str, optional): The character encoding of the file. Defaults to 'utf-8'.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file.

    Raises:
        None
    """
    # Use TextIOWrapper to ensure that the file is opened as a text file
    # rather than a binary file.
    csv_reader = csv.DictReader(TextIOWrapper(file, encoding='utf-8'))
    data = [row for row in csv_reader]
    return data
