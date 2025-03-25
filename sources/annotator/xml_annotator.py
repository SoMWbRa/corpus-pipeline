from abc import ABC, abstractmethod
from lxml import etree
from sources.annotator.abstract_annotator import AbstractAnnotator


class XMLAnnotator(AbstractAnnotator):
    """
    Annotator that creates XML documents using lxml.
    """

    def name(self) -> str:
        return "XML Annotator"

    def create_document(self, metadata):
        """
        Create a new XML document with metadata.

        Args:
            metadata: Document metadata

        Returns:
            XML Element representing the document
        """
        root = etree.Element("root")

        # Add metadata
        meta = etree.SubElement(root, "metadata")

        if metadata:
            etree.SubElement(meta, "title").text = metadata.title
            etree.SubElement(meta, "source").text = metadata.source

            if metadata.author:
                etree.SubElement(meta, "author").text = metadata.author

            if metadata.language:
                etree.SubElement(meta, "language").text = metadata.language

            if metadata.publication_time:
                etree.SubElement(meta, "publication_time").text = metadata.publication_time

        # Create document section
        etree.SubElement(root, "document")
        return root

    def add_heading(self, document, text):
        """
        Add a heading to the XML document.
        """
        doc_element = document.find("document")
        etree.SubElement(doc_element, "h").text = text
        return document

    def add_paragraph(self, document, text):
        """
        Add a paragraph to the XML document.
        """
        doc_element = document.find("document")
        etree.SubElement(doc_element, "p").text = text
        return document

    def add_list(self, document, items, ordered=False):
        """
        Add a list to the XML document.
        """
        doc_element = document.find("document")
        list_tag = "ol" if ordered else "ul"
        list_element = etree.SubElement(doc_element, list_tag)

        for item in items:
            etree.SubElement(list_element, "li").text = item

        return document

    def add_quote(self, document, text):
        """
        Add a quote to the XML document.
        """
        doc_element = document.find("document")
        etree.SubElement(doc_element, "quote").text = text
        return document

    def get_string(self, document):
        """
        Get the XML document as a formatted string.
        """
        return etree.tostring(document, pretty_print=True, encoding="unicode")