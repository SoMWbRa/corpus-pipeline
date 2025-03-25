import re
from typing import Tuple, List

from sources.normalizer.abstract_normalizer import AbstractNormalizer
from sources.normalizer.constants import Constants


class WhiteSpaceNormalizer(AbstractNormalizer):
    @staticmethod
    def name() -> str:
        return "WhiteSpaceNormalizer"

    @staticmethod
    def normalize(text: str) -> Tuple[str, List[str], List[str]]:
        warnings = []
        errors = []

        if "\t" in text:
            warnings.append("Text contains tabs, which were replaced with spaces.")

        regex_pattern = f'[\s{"".join(Constants.NON_BREAKING_SPACES)}]+'
        normalized_text = re.sub(regex_pattern, Constants.SPACE, text).strip()

        return normalized_text, warnings, errors
