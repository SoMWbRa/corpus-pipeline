
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

    def update_elements(self, document, update_fn):
        """
        Iterate through the document and update text in elements, including metadata.
        """
        pass

    def split_elements(self, document, split_s_fn, split_w_fn):
        """
        Iterate through the document p, q, h, li elements and split it into s and w elements.
        """

    def add_warnings(self, document, warnings):
        """
        Add warnings to the document.
        """
        pass

    def add_errors(self, document, errors):
        """
        Add errors to the document.
        """
        pass