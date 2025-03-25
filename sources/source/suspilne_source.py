from typing import Iterator

from sources.source.abstract_source import AbstractSource
from sources.record.abstract_record import Metadata
from sources.record.suspilne_record import SuspilneRecord


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
    def records() -> Iterator[SuspilneRecord]:
        """
        Return an iterator of records.
        """

        records = [
            SuspilneRecord(
                metadata=Metadata(
                    title="Як росіяни збирають інформацію про військовослужбовців з Полтавщини",
                    source="Суспільне Полтава",
                    author="Катерина Семисал",
                    language="uk",
                    publication_time="2025-01-13T13:36:00.000Z",
                ),
                link="https://suspilne.media/poltava/923947-ak-rosiani-zbiraut-informaciu-pro-vijskovosluzbovciv-z-poltavsini/",
            ),
        ]

        return iter(records)