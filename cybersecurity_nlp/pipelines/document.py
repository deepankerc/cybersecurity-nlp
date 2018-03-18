from cybersecurity_nlp.utils.text_cleaning import clean_text

class Document:

    def __init__(self, raw):
        self.id_= raw["id"]
        self._year = raw["year"]
        self._country = raw["country"]
        self._original_url = raw["original_url"]
        self._raw = raw["text"]

    @property
    def country(self):
        return self._country

    @property
    def raw(self):
        return self._raw

    def text(self):
        text = clean_text(self.raw)
        return text

    @property
    def url(self):
        return self._original_url

    @property
    def year(self):
        return self._year
