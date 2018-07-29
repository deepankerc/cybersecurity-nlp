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
    for doc in corpus.documents():
        doc_data.append({
            'id': doc.id(),
            'url': doc.url(),
            'country': doc.country(),
            'year': doc.year()
        })
        for sent in doc.sentences():
            sentence_data.append({
                'text': sent.text(),
                'id': sent.id(),
                'paragraph_id': sent.paragraph_id(),
                'doc_id': doc.id(),
                'indent': sent.requires_indentation(),
                'categories': sent.categories()
            })

    # Sort by position in doc
    sentence_data = sorted(
        sentence_data, key=lambda x: int(x['id'].split('_')[-1]))

    with open('app/src/assets/sentence_data.json', 'w') as f:
        f.write(json.dumps(sentence_data))
    with open('app/src/assets/doc_data.json', 'w') as f:
        f.write(json.dumps(doc_data))

if __name__ == '__main__':
    save_data_files()
