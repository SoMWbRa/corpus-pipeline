from typing import Tuple, List

from sources.normalizer.abstract_normalizer import AbstractNormalizer
from sources.normalizer.apostrophe_normalizer import ApostropheNormalizer
from sources.normalizer.quotation_marks_normalizer import QuotationMarksNormalizer
from sources.normalizer.ukrainian_phone_normalizer import UkrainianPhoneNormalizer
from sources.normalizer.white_space_normalizer import WhiteSpaceNormalizer


class NewsNormalizer(AbstractNormalizer):
    normalizers = [
        WhiteSpaceNormalizer,
        ApostropheNormalizer,
        QuotationMarksNormalizer,
        UkrainianPhoneNormalizer,
    ]

    @staticmethod
    def name() -> str:
        return "NewsNormalizer"

    @staticmethod
    def normalize(text: str, debug=False) -> Tuple[str, List[str], List[str]]:
        """Normalize the text and return it along with a list of warnings and errors."""
        warnings = []
        errors = []

        if debug:
            print("Initial text:\n", text)

        for normalizer in NewsNormalizer.normalizers:
            result = normalizer.normalize(text)
            text = result[0]
            warnings.extend(result[1])
            errors.extend(result[2])

            if debug:
                print(f"After {normalizer.name()}:\n", text)
                print("Warnings:\n", result[1])
                print("Errors:\n", result[2])

        return text, warnings, errors
