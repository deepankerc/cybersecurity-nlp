from cybersecurity_nlp.utils.text_cleaning import (clean_sentence,
    is_bad_sentence)

class Sentence(object):

    def __init__(self, sentence_id, paragraph_id, doc_id, text):
        self._id = sentence_id
        self._paragraph_id = paragraph_id
        self._doc_id = doc_id
        self._text = text

    def text(self):
        text = clean_sentence(self._text)
        return text

    def is_bad(self):
        return is_bad_sentence(self.text())

    def url(self):
        return self._original_url

    def year(self):
        return self._year
