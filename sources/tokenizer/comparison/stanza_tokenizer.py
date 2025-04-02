import stanza

from sources.tokenizer.abstract_tokenizer import AbstractTokenizer


class StanzaTokenizer(AbstractTokenizer):
    def __init__(self):
        self.nlp = stanza.Pipeline("uk", processors="tokenize")

    def name(self) -> str:
        return "stanza"

    def tokenize(self, text: str) -> list:
        doc = self.nlp(text)
        return [word.text for sent in doc.sentences for word in sent.words]