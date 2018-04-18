# This script generates the data files rendered by the application.

import json
import os
import sys

sys.path.append(os.getcwd()) # probably better to just pip install
from cybersecurity_nlp.pipelines.corpus import Corpus

def save_data_files():
    sentence_data = []
    doc_data = []
    corpus = Corpus()
    for doc in corpus.documents:
        doc_data.append({
            'id': doc.id,
            'url': doc.url,
            'country': doc.country
        })
        for sent in doc.sentences():
            if not sent.is_bad():
                sentence_data.append({
                    'text': sent.text(),
                    'doc_id': doc.id
                })
    with open('app/src/assets/sentence_data.json', 'w') as f:
        f.write(json.dumps(sentence_data))
    with open('app/src/assets/doc_data.json', 'w') as f:
        f.write(json.dumps(doc_data))

if __name__ == '__main__':
    save_data_files()
