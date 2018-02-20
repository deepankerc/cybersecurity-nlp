"""Class that wraps the document_key.csv file which contains metadata
about the docs"""

from collections import namedtuple
import csv
import os

class DocumentKey(object):
    """Wraps the document_key.csv file to provide simple access to the
    document metadata
    TODO: Add methods here as needed"""
    def __init__(self):
        self._set_path()
        self._parse_file()

    def _set_path(self):
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "document_key.csv")

    def _parse_file(self):
        rows = []
        with open(self.path, newline="") as infile:
            reader = csv.reader(infile)
            Row = namedtuple("Row", next(reader))
            for row in map(Row._make, reader):
                rows.append(row)
        self.rows = rows
