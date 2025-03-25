from abc import ABC, abstractmethod


class Metadata:
    """
    A class to store metadata about a text: source, author, title, language, publication time.
    """
    def __init__(self, source: str, author: str, title: str, language: str, publication_time: str):
        self.source = source
        self.author = author
        self.title = title
        self.language = language
        self.publication_time = publication_time


class AbstractRecord(ABC):
    """
      Class to represent a record with metadata and link to the source.
    """

    def __init__(self, metadata: Metadata, link: str):
        self.metadata = metadata
        self.link = link

    @abstractmethod
    def content(self) -> str:
        """
        Return the raw text of the record.
        """
        pass

