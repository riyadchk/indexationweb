from nltk.tokenize import word_tokenize


class Tokenizer:
    @staticmethod
    def tokenize(text):
        return word_tokenize(text)
