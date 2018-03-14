from cybersecurity_nlp.utils.text_cleaning import clean_text

class Document:

    def __init__(self, raw):
        self.id_= raw["id"]
        self.year = raw["year"]
        self.country = raw["country"]
        self.original_url = raw["original_url"]
        self.raw = raw["text"]

    def country(self):
        return self.country

    def raw_text(self):
        return self.raw

    def text(self):
        text = clean_text(self.raw_text())
        return text

    def url(self):
        return self.original_url

    def year(self):
        return self.year
