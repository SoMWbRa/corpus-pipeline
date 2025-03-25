from abc import ABC, abstractmethod


class AbstractSaver(ABC):

    @staticmethod
    def name() -> str:
        """
        Return the name of the saver.
        """
        pass

    @abstractmethod
    def save(self, text: str, name: str):
        """
        Save the text to the storage.
        """
        pass
