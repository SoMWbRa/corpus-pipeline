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
            SuspilneRecord(
                metadata=Metadata(
                    title="Найбільші країни ЄС не підтримують пропозицію виділити 20 млрд пакет допомоги Україні — топдипломат ЄС",
                    source="Суспільне Новини",
                    author="Олена Богданьок, Валерія Пашко",
                    language="uk",
                    publication_time="2025-03-26T10:42:00.000Z",
                ),
                link="https://suspilne.media/964001-veliki-kraini-es-ne-pidtrimuut-propoziciu-vidiliti-20-mlrd-paket-dopomogi-ukraini-topdiplomat-es/",
            ),
            SuspilneRecord(
                metadata=Metadata(
                    title="Весняний ярмарок, день відкритих дверей і виготовлення окопних свічок: куди піти в Миколаєві вихідними",
                    source="Суспільне Миколаїв",
                    author="Поліна Гожбур",
                    language="uk",
                    publication_time="2025-02-28T17:08:00.000Z",
                ),
                link="https://suspilne.media/mykolaiv/959899-vesnanij-armarok-den-vidkritih-dverej-i-vigotovlenna-okopnih-svicok-kudi-piti-v-mikolaevi-vihidnimi/",
            ),
        ]

        return iter(records)