from sources.corrector.abstract_corrector import AbstractCorrector


class NoChangesCorrector(AbstractCorrector):
    """
    A placeholder corrector that makes no changes to the text.
    This serves as a stub implementation for the Corrector component.
    """

    def correct(self, text: str, warnings: list, errors: list) -> (str, list, list):
        """
        Returns the original text without making any changes.

        Args:
            text: Text to correct
            warnings: List of warnings
            errors: List of errors

        Returns:
            Tuple of (unchanged_text, original_warnings, original_errors)
        """
        return text, warnings, errors
