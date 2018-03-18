from cybersecurity_nlp.data.document_accessor import DocumentAccessor
from cybersecurity_nlp.pipelines.document import Document

class Corpus(object):

    def __init__(self):
        raw_docs = DocumentAccessor().documents(from_file_only=True)
        docs = []
        for doc in raw_docs:
            docs.append(Document(doc))
        self._docs = docs

    @property
    def documents(self):
        return self._docs
