from cybersecurity_nlp.data.document_accessor import DocumentAccessor
from cybersecurity_nlp.pipelines.document import Document
from cybersecurity_nlp.utils.tokenization import SentenceTokenizer

class Corpus(object):

    def __init__(self):
        raw_docs = DocumentAccessor().documents(from_file_only=True)
        docs = []
        for doc in raw_docs:
            docs.append(Document(doc, self))
        self._docs = docs
        self._sentence_tokenizer = SentenceTokenizer()

    @property
    def documents(self):
        return self._docs

    @property
    def sentence_tokenizer(self):
        return self._sentence_tokenizer
