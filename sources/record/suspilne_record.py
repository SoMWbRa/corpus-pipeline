import requests
from bs4 import BeautifulSoup

from sources.record.abstract_record import AbstractRecord, Metadata


class SuspilneRecord(AbstractRecord):
    def __init__(self, metadata: Metadata, link: str):
        super().__init__(metadata, link)
        self._content = None

    def fetch_metadata(self, soup: BeautifulSoup):
        """
        Fetch missed author metadata from the article.
        """
        # Try first to find author in meta tags
        author_element = soup.find("meta", {"name": "author"})
        if author_element:
            self.metadata.author = author_element["content"]
            return

    def content(self) -> str:
        """
        Download the content of the article if it is not downloaded yet.
        """
        if self._content is None:
            response = requests.get(self.link, timeout=10)
            response.raise_for_status()
            self._content = response.text

            soup = BeautifulSoup(self._content, "html.parser")
            self.fetch_metadata(soup)

        return self._content

