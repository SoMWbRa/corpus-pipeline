import nltk

from sources.tokenizer.abstract_tokenizer import AbstractTokenizer


class NTLKTokenizer(AbstractTokenizer):
    def name(self) -> str:
        return "nltk"

    def tokenize(self, text: str) -> list:
        return nltk.word_tokenize(text)
