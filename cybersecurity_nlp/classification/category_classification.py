"""Class for predicting the category of a sentence

I attempted to use Snorkel to gather training data, but it wasn't clear that
I would be able to outperform simple regex classifiers. Perhaps that's an area
of further exploration, but for now I'll stick with regexes.
"""
import re

CATEGORY_CLASSIFIER = None

def make_regex(terms, force_end_boundary=False):
    pattern = '(^|\\b)' + '|'.join(map(lambda x: '(' + x + ')', terms))
    if force_end_boundary:
        pattern += '(\\b)'
    return pattern

CATEGORY_REGEXES = {
    "Legal Measures": [
        (make_regex(['legislation', 'legal', 'law', 'regulation',
                     'compliance']), True),
        (make_regex(['Act'], force_end_boundary=True), False),
    ],
    "Technical Measures": [
        (make_regex(['cirt', 'cyber incident response team', 'certification']),
         True)
    ],
    "Organization Measures": [
        (make_regex(['policy', 'roadmap', 'responsible agency',
                     'benchmarking']), True)
    ],
    "Capacity Building": [
        (make_regex(['hiring', 'certification']), True),
        (make_regex(['hire'], force_end_boundary=True), True)
    ],
    "Cooperation": [
        (make_regex(['cooperation']), True)
    ],
    "Child Online Protection": [
        (make_regex(['child', 'kids']), True)
    ]
}

class CategoryClassifier(object):
    def __init__(self):
        pass
    def predict(self, sentence):
        categories = []
        for category, patterns in CATEGORY_REGEXES.items():
            for pattern, ignore_case in patterns:
                if ignore_case:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        categories.append(category)
                        break
                else:
                    if re.search(pattern, sentence):
                        categories.append(category)
                        break
        return categories

def get_category_classifier():
    global CATEGORY_CLASSIFIER
    if CATEGORY_CLASSIFIER is None:
        CATEGORY_CLASSIFIER = CategoryClassifier()
        return CATEGORY_CLASSIFIER
    else:
        return CATEGORY_CLASSIFIER
