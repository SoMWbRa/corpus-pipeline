import requests

from sources.record.abstract_record import AbstractRecord


class SuspilneRecord(AbstractRecord):
    def content(self) -> str:
        """
        Return the raw html text of the record.
        """
        response = requests.get(self.link, timeout=10)
        response.raise_for_status()
        return response.text
