"""Class for accessing the raw documents"""

from collections import namedtuple
import csv
import os
from pdfminer.pdftypes import PDFException

from cybersecurity_nlp.data.extract_text import convert_pdf_to_text
from cybersecurity_nlp import logger

class DocumentAccessor(object):
    """Class for accessing raw documents

    This class parses the `cybersecurity_nlp/data/document_key.csv` file and
    looks in `cybersecurity_nlp/data/raw` for the raw pdfs to transform. This
    assumes that `download_documents.sh` has been run first.
    """
    def __init__(self):
        self._set_paths()
        self._parse_file()

    def _set_paths(self):
        self.key_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "document_key.csv")
        self.raw_doc_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "raw")
        self.text_doc_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "text")

    def _parse_file(self):
        rows = []
        logger.info("Parsing key file")
        with open(self.key_path, newline="") as infile:
            reader = csv.reader(infile)
            Row = namedtuple("Row", next(reader))
            for row in map(Row._make, reader):
                rows.append(row)
        logger.info("%d documents found in key file", len(rows))
        self.rows = rows

    def documents(self, from_file_only=False):
        """Get all documents in dict form

        Params
        ------
        from_file_only: bool
            If True, get documents from saved txt files only. Otherwise, this
            will run the text extraction on all pdfs that haven't already been
            converted to txt.

        Returns
        -------
        list
            List of dicts representing the documents.
        """
        docs = []
        for i, row in enumerate(self.rows):
            # No language support, so skip non-english documents
            if row.Language != "EN":
                continue
            text = None
            text_file = os.path.join(self.text_doc_path, row.File + ".txt")
            if os.path.isfile(text_file):
                logger.info("Reading %s from text file", row.File)
                with open(text_file, "r") as f:
                    text = f.read()
            elif not from_file_only:
                logger.info("Converting %s to text", row.File)
                try:
                    text = convert_pdf_to_text(
                        os.path.join(self.raw_doc_path, row.File))
                except TimeoutError:
                    logger.warning("Timed out converting pdf %s" % row.File)
                    continue
                except PDFException:
                    logger.warning("Error converting pdf %s" % row.File)
                    continue
                with open(text_file, "w") as f:
                    f.write(text)
            else:
                logger.warning("Skipping pdf %s" % row.File)
            if text is not None:
                docs.append({
                    "id": i,
                    "country": row.Country,
                    "year": row.Year,
                    "original_url": row.OriginalURL,
                    "text": text
                })
        return docs
