from nltk.stem import PorterStemmer


class Stemmer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]
