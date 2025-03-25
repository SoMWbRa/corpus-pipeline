from bs4 import BeautifulSoup, Tag
from typing import List, Any

from sources.annotator.abstract_annotator import AbstractAnnotator
from sources.record.abstract_record import Metadata
from sources.record.suspilne_record import SuspilneRecord


class SuspilneParser:
    """
    Parser for Suspilne HTML content.
    """

    @staticmethod
    def name() -> str:
        """
        Return the name of the parser.
        """
        return "Parser for \"Суспільне Новини | Suspilne Novyny\""


    @staticmethod
    def parse(content: str, metadata: Metadata, annotator: AbstractAnnotator) -> Any:
        """
        Parse HTML content from Suspilne and create a document using the provided annotator.

        Args:
            content: HTML content to parse
            metadata: Metadata for the document
            annotator: Annotator to use for document creation

        Returns:
            Document created by the annotator
        """
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Find the main content container - this is the selector specific to Suspilne
        content_container = soup.select_one("div.l-article-content__container-inner.c-art-c__c")

        if not content_container:
            # Try alternative selectors if the main one fails
            content_container = soup.select_one("div.article-text") or \
                                soup.select_one("div.content-blocks")

            if not content_container:
                raise ValueError("Failed to find main content container in the HTML")

        document = annotator.create_document(metadata=metadata)

        SuspilneParser._process_content_elements(content_container, annotator, document)

        return document

    @staticmethod
    def _process_content_elements(container: Tag, annotator: Any, document: Any) -> None:
        """
        Process content elements from the HTML and add them to the document.

        Args:
            container: BeautifulSoup Tag containing the content elements
            annotator: Annotator to use for document creation
            document: Document to add elements to
        """
        for element in container.children:
            # Skip non-tag elements like NavigableString
            if not isinstance(element, Tag):
                continue

            tag_name = element.name

            # Process different types of content elements
            if tag_name and tag_name.startswith('h') and len(tag_name) == 2:
                # Heading elements (h1, h2, h3, etc.)
                annotator.add_heading(document, element.get_text(strip=True))

            elif tag_name == 'p':
                # Paragraph elements
                text = element.get_text(strip=True)
                if text:  # Only add non-empty paragraphs
                    annotator.add_paragraph(document, text)

            elif tag_name == 'ul':
                # Unordered list elements
                items = [li.get_text(strip=True) for li in element.find_all('li', recursive=False)]
                if items:  # Only add non-empty lists
                    annotator.add_list(document, items, ordered=False)

            elif tag_name == 'ol':
                # Ordered list elements
                items = [li.get_text(strip=True) for li in element.find_all('li', recursive=False)]
                if items:  # Only add non-empty lists
                    annotator.add_list(document, items, ordered=True)

            elif tag_name == 'blockquote':
                # Quote elements
                annotator.add_quote(document, element.get_text(strip=True))

            elif tag_name == 'div':
                # Process div elements recursively if they might contain content
                if 'class' in element.attrs and any(c in element.attrs['class'] for c in ['content-block', 'article-paragraph']):
                    SuspilneParser._process_content_elements(element, annotator, document)
                # Also process divs that contain other content elements
                elif element.find(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'blockquote']):
                    SuspilneParser._process_content_elements(element, annotator, document)