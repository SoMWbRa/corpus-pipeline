import os

from sources.saver.abstract_saver import AbstractSaver


class FileSaver(AbstractSaver):
    def __init__(self, path: str, create_dir: bool = True):
        self.path = path

        if create_dir and not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def name() -> str:
        return "File Saver"

    def save(self, text: str, name: str):
        with open(f"{self.path}/{name}", "w") as file:
            file.write(text)

