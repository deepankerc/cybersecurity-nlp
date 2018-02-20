"""Convert pdfs to machine readable text"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_text(path):
    """Converts pdf at path to string with text representation
    TODO: Retain page numbers"""
    resource_manager = PDFResourceManager()
    out = StringIO()
    laparams = LAParams()
    device = TextConverter(
        resource_manager, out, codec='utf-8', laparams=laparams)
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(
                fp, set(), maxpages=0, password='', caching=True,
                check_extractable=True):
            interpreter.process_page(page)            
        text = out.getvalue()

    device.close()
    out.close()
    return text
