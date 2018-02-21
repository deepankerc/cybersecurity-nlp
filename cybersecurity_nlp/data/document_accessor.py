"""Class for accessing the raw documents"""

from collections import namedtuple
import csv
import os

from cybersecurity_nlp.data.extract_text import convert_pdf_to_text

class DocumentAccessor(object):
    """Class for accessing raw documents"""
    def __init__(self):
        self._set_paths()
        self._parse_file()

    def _set_paths(self):
        self.key_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "document_key.csv")
        self.doc_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "raw")

    def _parse_file(self):
        rows = []
        with open(self.key_path, newline="") as infile:
            reader = csv.reader(infile)
            Row = namedtuple("Row", next(reader))
            for row in map(Row._make, reader):
                rows.append(row)
        self.rows = rows

    def documents(self):
        docs = []
        for i, row in enumerate(self.rows):
            print("Opening: ", os.path.join(self.doc_path, row.File))
            docs.append({
                "id": i,
                "country": row.Country,
                "year": row.Year,
                "original_url": row.OriginalURL,
                "text": convert_pdf_to_text(
                    os.path.join(self.doc_path, row.File))
            })
        return docs
