
from abc import ABC, abstractmethod


class AbstractAnnotator(ABC):
    """
    Abstract class for document annotation.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Return the name of the annotator.
        """
        pass

    @abstractmethod
    def create_document(self, metadata):
        """
        Create a new document with metadata.

        Args:
            metadata: Document metadata

        Returns:
            Document object
        """
        pass

    @abstractmethod
    def add_heading(self, document, text):
        """
        Add a heading to the document.

        Args:
            document: Document to add heading to
            text: Heading text

        Returns:
            Updated document
        """
        pass

    @abstractmethod
    def add_paragraph(self, document, text):
        """
        Add a paragraph to the document.

        Args:
            document: Document to add paragraph to
            text: Paragraph text

        Returns:
            Updated document
        """
        pass

    @abstractmethod
    def add_list(self, document, items, ordered=False):
        """
        Add a list to the document.

        Args:
            document: Document to add list to
            items: List items
            ordered: Whether the list is ordered

        Returns:
            Updated document
        """
        pass

    @abstractmethod
    def add_quote(self, document, text):
        """
        Add a quote to the document.

        Args:
            document: Document to add quote to
            text: Quote text

        Returns:
            Updated document
        """
        pass

    @abstractmethod
    def get_string(self, document) -> str:
        """
        Get the result document.

        Args:
            document: Document to get result from

        Returns:
            Result document
        """
        pass