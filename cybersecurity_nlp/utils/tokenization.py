from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

class SentenceTokenizer(PunktSentenceTokenizer):
    """
    Sentence tokenizer extends the punkt tokenizer so that it can be customized
    """    
    def __init__(self):
        punkt_param = PunktParameters()
        punkt_param.abbrev_types = set(['e.g', 'ie', 'i.e', 'eg'])
        super().__init__(punkt_param)
