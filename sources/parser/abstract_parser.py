from abc import ABC, abstractmethod


class AbstractParser(ABC):
    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Return the name of the parser.
        """
        pass

    @staticmethod
    @abstractmethod
    def parse(text: str) -> str:
        """
        Parse the input text and return the parsed document.
        """
        pass
