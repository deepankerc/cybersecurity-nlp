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
        '''Sentence ID is of the form {{ doc id }}_{{ sentence index}}'''
        self._paragraph_idx = idx
        self._paragraph_id = self._doc_id + "_" + str(idx)

    def paragraph_id(self):
        return self._paragraph_id

    def url(self):
        return self._original_url

    def year(self):
        return self._year
