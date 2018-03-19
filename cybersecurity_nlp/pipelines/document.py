from cybersecurity_nlp.pipelines.sentence import Sentence
from cybersecurity_nlp.utils.text_cleaning import clean_text

class Document(object):

    def __init__(self, raw, corpus):
        self._id = raw["id"]
        self._year = raw["year"]
        self._country = raw["country"]
        self._original_url = raw["original_url"]
        self._raw = raw["text"]
        self._corpus = corpus

    @property
    def corpus(self):
        return self._corpus

    @property
    def country(self):
        return self._country

    @property
    def id(self):
        return self._id

    @property
    def raw(self):
        return self._raw

    def text(self):
        text = clean_text(self.raw)
        return text

    @property
    def url(self):
        return self._original_url

    @property
    def year(self):
        return self._year

    def sentences(self):
        sentences = []
        raw_sentences = self.corpus.sentence_tokenizer.tokenize(self.text())
        for i, sent in enumerate(raw_sentences):
            sentences.append(Sentence(i, 0, self.id, sent))
        return sentences
