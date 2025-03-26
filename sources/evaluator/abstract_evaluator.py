from typing import List, Tuple
from abc import ABC, abstractmethod


class AbstractEvaluator:
    """
    Abstract class for evaluation of text errors.
    """
    @abstractmethod
    def name(self) -> str:
        """
        Return the name of the evaluator.
        """
        pass

    @abstractmethod
    def evaluate(self, text) -> Tuple[List[str], List[str]]:
        """
        Evaluate the text for errors.

        Returns: Tuple of lists of warnings and errors
        """
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
