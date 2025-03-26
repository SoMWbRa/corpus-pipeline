from typing import Tuple, List
from sources.evaluator.abstract_evaluator import AbstractEvaluator
import language_tool_python


class LanguageToolEvaluator(AbstractEvaluator):
    def __init__(self):
        self.tool = None

    def name(self) -> str:
        return "Simple Evaluator"

    def evaluate(self, text) -> Tuple[List[str], List[str]]:
        """
        Evaluate the text for errors.

        Returns: Tuple of lists of warnings and errors
        """
        warnings = []
        errors = []

        matches = self.tool.check(text)

        for match in matches:
            replacements = ", ".join(match.replacements)
            warnings.append(f"Message: {match.message} Offset: {match.offset}. Replacement: {replacements}")

        return warnings, errors

    def __enter__(self):
        self.tool = language_tool_python.LanguageTool('uk-UA')
        print(self.tool._url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tool.close()


if __name__ == "__main__":
    with LanguageToolEvaluator() as evaluator:
        warnings, errors = evaluator.evaluate("В вагоні було тихо. У очах його була радість. Мати і діти сиділи разом.")
        print(warnings)
        print(errors)

# %%
