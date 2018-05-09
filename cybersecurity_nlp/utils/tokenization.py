import re

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

class SentenceTokenizer(PunktSentenceTokenizer):
    """A custom sentence tokenizer that extends the punkt tokenizer so that it
    can be customized to this project"""
    def __init__(self):
        punkt_param = PunktParameters()
        punkt_param.abbrev_types = set(['e.g', 'ie', 'i.e', 'eg'])
        super().__init__(punkt_param)

    def tokenize(self, text):
        tokenized_sentences = super().tokenize(text)
        final_tokenized_sentences = []
        for sentence in tokenized_sentences:
            header = re.match(r'(([^a-z ]+)\s+){3,}', sentence)
            if header:
                end = header.end()
                final_tokenized_sentences.extend([
                    sentence[:end].strip(),
                    sentence[end:].strip()
                ])
            else:
                final_tokenized_sentences.append(sentence)
        return final_tokenized_sentences
