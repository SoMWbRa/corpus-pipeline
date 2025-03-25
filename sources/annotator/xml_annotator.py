from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import xml.dom.minidom

from sources.annotator.abstract_annotator import AbstractAnnotator


class XMLAnnotator(AbstractAnnotator):
    """
    Annotator that creates XML documents.
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
        root = ET.Element("root")

        # Add metadata
        meta = ET.SubElement(root, "metadata")

        # Add metadata if provided
        if metadata:
            ET.SubElement(meta, "title").text = metadata.title
            ET.SubElement(meta, "source").text = metadata.source

            if metadata.author:
                ET.SubElement(meta, "author").text = metadata.author

            if metadata.language:
                ET.SubElement(meta, "language").text = metadata.language

            if metadata.publication_time:
                ET.SubElement(meta, "publication_time").text = metadata.publication_time

        # Create document section
        document = ET.SubElement(root, "document")

        # Return root element that contains both metadata and document
        return root

    def add_heading(self, document, text):
        """
        Add a heading to the XML document.

        Args:
            document: XML Element representing the document
            text: Heading text

        Returns:
            XML Element with added heading
        """
        doc_element = document.find("document")
        ET.SubElement(doc_element, "h").text = text
        return document

    def add_paragraph(self, document, text):
        """
        Add a paragraph to the XML document.

        Args:
            document: XML Element representing the document
            text: Paragraph text

        Returns:
            XML Element with added paragraph
        """
        doc_element = document.find("document")
        ET.SubElement(doc_element, "p").text = text
        return document

    def add_list(self, document, items, ordered=False):
        """
        Add a list to the XML document.

        Args:
            document: XML Element representing the document
            items: List items
            ordered: Whether the list is ordered

        Returns:
            XML Element with added list
        """
        doc_element = document.find("document")
        list_tag = "ol" if ordered else "ul"
        list_element = ET.SubElement(doc_element, list_tag)

        for item in items:
            ET.SubElement(list_element, "li").text = item

        return document

    def add_quote(self, document, text):
        """
        Add a quote to the XML document.

        Args:
            document: XML Element representing the document
            text: Quote text

        Returns:
            XML Element with added quote
        """
        doc_element = document.find("document")
        ET.SubElement(doc_element, "quote").text = text
        return document

    def get_string(self, document):
        """
        Get the XML document as a string.

        Args:
            document: XML Element representing the document

        Returns:
            String representation of the XML document
        """
        rough_string = ET.tostring(document, 'utf-8')
        dom = xml.dom.minidom.parseString(rough_string)
        return dom.toprettyxml(indent="    ")
