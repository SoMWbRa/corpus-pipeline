import tempfile
import os
import xml.etree.ElementTree as ET

from sources.tokenizer.abstract_tokenizer import AbstractTokenizer


class LanguageToolTokenizer(AbstractTokenizer):
    def name(self) -> str:
        return "language_tool"

    def tokenize(self, text: str) -> list:
        file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        file.write(text)
        file.close()

        command = f"python3 language_tool/tokenize_text.py -o {file.name} {file.name}"
        os.system(command)

        with open(file.name, "r", encoding="utf-8") as file:

            tree = ET.parse(file)

            root = tree.getroot()
            tokens = []

            for sentence in root.iter('sentence'):
                for token in sentence.iter('token'):
                    tokens.append(token.text)

            return tokens


