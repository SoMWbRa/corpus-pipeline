import datetime
from typing import Iterator
from bs4 import BeautifulSoup
import requests

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
    def records(mock: bool = False) -> Iterator[SuspilneRecord]:
        """
        Return an iterator of records.
        """

        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        # https://suspilne.media/archive/2025/3/25/
        archive_url = f"https://suspilne.media/archive/{yesterday.year}/{yesterday.month}/{yesterday.day}/"

        records = []

        if mock:
            records = [
                SuspilneRecord(
                    metadata=Metadata(
                        title="Як росіяни збирають інформацію про військовослужбовців з Полтавщини",
                        source="Суспільне Полтава",
                        author="Катерина Семисал",
                        language="uk",
                        publication_time="2025-01-13T13:36:00.000Z",
                        reference="https://suspilne.media/poltava/923947-ak-rosiani-zbiraut-informaciu-pro-vijskovosluzbovciv-z-poltavsini/",
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
                        reference="https://suspilne.media/964001-veliki-kraini-es-ne-pidtrimuut-propoziciu-vidiliti-20-mlrd-paket-dopomogi-ukraini-topdiplomat-es/",
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
                        reference="https://suspilne.media/mykolaiv/959899-vesnanij-armarok-den-vidkritih-dverej-i-vigotovlenna-okopnih-svicok-kudi-piti-v-mikolaevi-vihidnimi/",
                    ),
                    link="https://suspilne.media/mykolaiv/959899-vesnanij-armarok-den-vidkritih-dverej-i-vigotovlenna-okopnih-svicok-kudi-piti-v-mikolaevi-vihidnimi/",
                ),
                SuspilneRecord(
                    metadata=Metadata(
                        title='"Жора нас прикрив". Бій за Малу Рогань став останнім для Георгія Тарасенка: спогади про звільнення села',
                        source="Суспільне Харків",
                        author="Альона Рязанцева, Лариса Говина",
                        language="uk",
                        publication_time="2025-03-25T16:33:00.000Z",
                        reference="https://suspilne.media/kharkiv/424830-boi-za-zvilnenna-maloi-rogani-na-harkivsini-rik-potomu/",
                    ),
                    link="https://suspilne.media/kharkiv/424830-boi-za-zvilnenna-maloi-rogani-na-harkivsini-rik-potomu/"
                )
            ]

            return iter(records)

        # Download the archive page

        request = requests.get(archive_url)
        request.raise_for_status()

        soup = BeautifulSoup(request.text, "html.parser")
        articles = soup.find_all("a", class_="c-article-card--small-headline")

        for article in articles:
            title = article.find("span", class_="c-article-card__headline-inner").text.strip()
            link = article["href"]
            publication_time = article.find("time")["datetime"]

            records.append(
                SuspilneRecord(
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
            )

        return iter(records)