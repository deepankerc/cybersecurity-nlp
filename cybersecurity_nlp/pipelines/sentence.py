import re

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
        '''Sentence ID is of the form {{ doc id }}_{{ sentence index}}'''
        return self._doc_id + "_" + str(self._sentence_idx)

    def is_bad(self):
        return is_bad_sentence(self.text())

    def assign_paragraph(self, idx):
        '''Paragraph ID is of the form {{ doc id }}_{{ paragraph index }}'''
        self._paragraph_idx = idx
        self._paragraph_id = self._doc_id + "_" + str(idx)

    def paragraph_id(self):
        return self._paragraph_id

    def url(self):
        return self._original_url

    def year(self):
        return self._year

    def requires_indentation(self):
        '''Indicates whether a new line is necessary when displaying the
        sentence in the context of a paragraph

        Sentences starting with things like '(1)', 'a)', or bullets should
        be indented to improve readability.
        '''
        bullets = set(['\u2022', '\u2023', '\u25e6', '\u2043', '\u2219'])
        if re.match(r'\(?[a-zA-Z0-9][\)|\.]', self.text()) or \
                self.text()[0] in bullets:
            return True
        else:
            return False
