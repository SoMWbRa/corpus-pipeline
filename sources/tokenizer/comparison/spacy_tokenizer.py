import spacy

from sources.tokenizer.abstract_tokenizer import AbstractTokenizer


class SpacyTokenizer(AbstractTokenizer):
    def __init__(self):
        self.nlp = spacy.load("uk_core_news_sm", enable=["parser"])

    def name(self) -> str:
        return "spacy"

    def tokenize(self, text: str) -> list:
        doc = self.nlp(text)
        return [token.text for token in doc]

