import csv
from io import TextIOWrapper

def read_csv(file):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    """
    # Use TextIOWrapper to ensure that the file is opened as a text file
    # rather than a binary file.
    csv_reader = csv.DictReader(TextIOWrapper(file))
    data = [row for row in csv_reader]
    return data
