from abc import ABC, abstractmethod
from typing import Iterator
from sources.record.abstract_record import AbstractRecord


class AbstractSource(ABC):
    """
    Abstract class for the data source. Return an iterator of records.
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Return the name of the source.
        """
        pass

    @staticmethod
    @abstractmethod
    def records() -> Iterator[AbstractRecord]:
        """
        Return an iterator of records.
        """
        pass
