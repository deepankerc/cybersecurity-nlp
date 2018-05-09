from cybersecurity_nlp.data.document_accessor import DocumentAccessor
from cybersecurity_nlp.pipelines.document import Document
from cybersecurity_nlp.utils.tokenization import SentenceTokenizer

class Corpus(object):

    def __init__(self, from_file_only=True):
        """Initialize corpus object

        Params
        ------
        from_file_only: bool
            Forwarded to DocumentAccessor.documents()
        """
        raw_docs = DocumentAccessor().documents(from_file_only=from_file_only)
        docs = []
        for doc in raw_docs:
            docs.append(Document(doc, self))
        self._docs = docs
        self._sentence_tokenizer = SentenceTokenizer()

    def documents(self):
        """Returns list of documents of type Document in the corpus"""
        return self._docs

    def sentence_tokenizer(self):
        """Returns instane of the sentence tokenizer to use throughout the
        pipeline"""
        return self._sentence_tokenizer
