import re

def clean_text(text):
    """Normalizes unicode characters and makes other safe cleaning
    improvements"""

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


def clean_sentence(text):
    """Fixes spacing within a sentence"""

    # strip leading/trailing whitespace
    text = text.strip()

    # replace new lines with spaces
    text = re.sub("\n", " ", text)

    # replace multiple spaces with single space
    text = re.sub("\s{2,}", " ", text)

    return text


def is_bad_sentence(text):
    """Decides if a sentence is bad (headers, too short, incomplete, etc)"""
    if len(text) < 20 or len(text) > 350:
        return True

    if float(len(re.findall("[a-zA-Z ]", text))) / len(text) < .85:
        return True

    if float(len(re.findall("[A-Z]", text))) / len(text) > .5:
        return True

    return False
