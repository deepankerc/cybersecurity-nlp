import re

def clean_text(text):
    # spacing
    text = re.sub("\xa0", " ", text)

    # quotes
    text = re.sub("\u201c|\u201d", '"', text)
    text = re.sub("\u2019|\u2018", "'", text)

    # bullet
    text = re.sub("\u25a0", "\u2022", text)

    # dashes
    text = re.sub("\u2010|\u2011|\u2012|\u2013|\u2014|\xad", "-", text)

    # replace newlines that obviously appear in the middle of sentences to
    # assist with sentence tokenization
    text = re.sub("(?<=[a-z\-,]) ?\n(?=[\(a-zA-Z1-9])", " ", text)

    return text
