import datetime
from typing import Iterator
from bs4 import BeautifulSoup
import requests

from sources.source.abstract_source import AbstractSource
from sources.record.abstract_record import Metadata
from sources.record.suspilne_record import SuspilneRecord
from sources.utils.daterange import daterange


class SuspilneSource(AbstractSource):
    """
    A class to represent a source of news from Suspilne Novyny.
    """

    @staticmethod
    def name() -> str:
        """
        Return the name of the source.
        """
        return "Суспільне Новини | Suspilne Novyny"

    @staticmethod
    def records(start: datetime, end: datetime):
        """
        Return an iterator of records.
        """

        for date in daterange(start, end):
            archive_url = f"https://suspilne.media/archive/{date.year}/{date.month}/{date.day}/"
            print(f"Processing: {archive_url}")

            request = requests.get(archive_url)
            request.raise_for_status()

            soup = BeautifulSoup(request.text, "html.parser")
            articles = soup.find_all("a", class_="c-article-card--small-headline")
            for article in articles:
                title = article.find("span", class_="c-article-card__headline-inner").text.strip()
                link = article["href"]
                publication_time = article.find("time")["datetime"]

                yield SuspilneRecord(
                    metadata=Metadata(
                        title=title,
                        source=SuspilneSource.name(),
                        author=None,
                        language="uk",
                        publication_time=publication_time,
                        reference=link,
                    ),
                    link=link,
                )
