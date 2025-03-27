from abc import ABC, abstractmethod


class AbstractTokenizer(ABC):

    def name(self) -> str:
        """
        Return the name of the tokenizer.
        """
        pass

    @abstractmethod
    def tokenize(self, text: str) -> list:
        """
        Tokenize the text.
        """
        pass
