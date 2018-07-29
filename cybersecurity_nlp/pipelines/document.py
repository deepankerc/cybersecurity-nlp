from functools import partial
from textacy import Doc
from textacy.keyterms import sgrank

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

    def corpus(self):
        return self._corpus

    def country(self):
        return self._country

    def doc(self):
        # NOTE: Should cache this somehow if we want to use for more than one
        # thing.
        return Doc(self.text(), lang="en")

    def id(self):
        return str(self._id)

    def key_terms(self, **kwargs):
        key_terms = partial(
            sgrank, ngrams=(1, 2, 3, 4), window_width=100, n_keyterms=20)
        return key_terms(self.doc(), **kwargs)

    def raw(self):
        return self._raw

    def text(self):
        text = clean_text(self.raw())
        return text

    def url(self):
        return self._original_url

    def year(self):
        return self._year

    def sentences(self, remove_bad=True):
        """Retrieve a list of sentences in the document

        Params
        ------
        remove_bad: bool
            If True, remove "bad" sentences (sentences that probably aren't
            meaningful and readable sentences).

        Returns
        -------
        list
            List of sentences of type Sentence in the document.
        """
        sentences = []
        raw_sentences = (self.corpus().sentence_tokenizer()
                            .tokenize(self.text()))
        # define paragraphs as runs of clean sentences
        paragraph_idx = 0
        for i, sent in enumerate(raw_sentences):
            s = Sentence(i, self.id(), sent)
            if s.is_bad():
                paragraph_idx += 1
            else:
                s.assign_paragraph(paragraph_idx)
            if not remove_bad or not s.is_bad():
                sentences.append(s)
        return sentences
