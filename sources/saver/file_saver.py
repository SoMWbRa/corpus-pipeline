from sources.saver.abstract_saver import AbstractSaver


class FileSaver(AbstractSaver):
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def name() -> str:
        return "File Saver"

    def save(self, text: str, name: str):
        with open(f"{self.path}/{name}.txt", "w") as file:
            file.write(text)

