import string
from nltk.tokenize import word_tokenize


class Tokenizer:
    @staticmethod
    def tokenize(text):
        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = word_tokenize(text)

        return [word.lower() for word in text if word.isalpha()]
