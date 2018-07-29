import re

from cybersecurity_nlp.classification.category_classification import (
    get_category_classifier)
from cybersecurity_nlp.utils.text_cleaning import (clean_sentence,
    is_bad_sentence)

class Sentence(object):

    def __init__(self, sentence_idx, doc_id, text):
        self._sentence_idx = sentence_idx
        self._doc_id = doc_id
        self._text = text
        self._paragraph_idx = None
        self._paragraph_id = None

    def text(self):
        text = clean_sentence(self._text)
        return text

    def id(self):
        """Returns a unique id associated with the sentence of the form x_y
        where x is the doc id and y is the sentence index in the doc."""
        return self._doc_id + "_" + str(self._sentence_idx)

    def is_bad(self):
        """Returns a boolean value specifying whether the sentence is "bad"""
        return is_bad_sentence(self.text())

    def assign_paragraph(self, idx):
        """Assigns a unique id associated with the paragraph of the sentence
        of the form x_y where x is the doc id and y is the paragraph index."""
        self._paragraph_idx = idx
        self._paragraph_id = self._doc_id + "_" + str(idx)

    def paragraph_id(self):
        return self._paragraph_id

    def url(self):
        return self._original_url

    def year(self):
        return self._year

    def categories(self):
        return get_category_classifier().predict(self.text())

    def requires_indentation(self):
        """Indicates whether a new line is necessary when displaying the
        sentence in the context of a paragraph

        Sentences starting with things like '(1)', 'a)', or bullets should
        be indented to improve readability.
        """
        bullets = set(['\u2022', '\u2023', '\u25e6', '\u2043', '\u2219'])
        if re.match(r'\(?[a-zA-Z0-9][\)|\.]', self.text()) or \
                self.text()[0] in bullets:
            return True
        else:
            return False
