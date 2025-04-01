from abc import ABC, abstractmethod


class AbstractCorrector(ABC):
    """
    Abstract class for text correction.
    """

    @abstractmethod
    def correct(self, text: str, warnings: list, errors: list) -> (str, list, list):
        """
        Correct the text based on identified errors and warnings.

        Args:
            text: Text to correct
            warnings: List of warnings
            errors: List of errors

        Returns:
            Tuple of (corrected_text, remaining_warnings, remaining_errors)
        """
        pass