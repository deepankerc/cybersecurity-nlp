# This script generates and parses files for use with AutoPhrase. AutoPhrase
# is a method for automated detection of key phrases in text.
# https://github.com/shangjingbo1226/AutoPhrase
#
# AutoPhrase accepts as input a file representing a corpus with one document
# on each line. This script generates that file:
#   python scripts/autophrase.tx --train > autophrase_training.txt
# 
# AutoPhrase will output a list of ranked phrases. This script will accept as
# input that list, dedupe it by stemming, and produce JSOn that can be fed into
# the app's search autocomplete:
#   python scripts/autophrase.tx --test autophrase_out.txt > autocomplete.json
import json
import csv
from argparse import ArgumentParser
from nltk.stem.porter import PorterStemmer
import os
import sys

sys.path.append(os.getcwd()) # probably better to just pip install
from cybersecurity_nlp.pipelines.corpus import Corpus

stemmer = PorterStemmer()


def stem_phrase(phrase):
    return ' '.join(map(lambda x: stemmer.stem(x), phrase.split()))


def train():
    c = Corpus()
    for doc in c.documents():
        for sentence in doc.sentences():
            print(json.dumps(sentence.text()))


def test(file_path):
    top_phrases = []
    top_stemmed_phrases = set()
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for score, phrase in reader:
            stemmed_phrase = stem_phrase(phrase)
            if float(score) < .8:
                break
            if stemmed_phrase not in top_stemmed_phrases:
                top_stemmed_phrases.add(stemmed_phrase)
                top_phrases.append(phrase)
    print(json.dumps(top_phrases))

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--train', action='store_true',
                        help='Generate training file for Autophrase.')
    parser.add_argument('--test', help='Path to output file from Autophrase.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    if args.train:
        train()
    if args.test:
        test(args.test)
