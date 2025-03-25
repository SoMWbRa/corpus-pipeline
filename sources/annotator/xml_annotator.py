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
        etree.SubElement(doc_element, "q").text = text
        return document

    def get_string(self, document):
        """
        Get the XML document as a formatted string.
        """
        return etree.tostring(document, pretty_print=True, encoding="unicode")

    def update_elements(self, document, update_fn):
        """
        Iterate through the document and update text in elements.

        Args:
            document: The XML document.
            update_fn: A function that takes a string and returns an updated string.

        Returns:
            The updated XML document.
        """
        doc_element = document.find("document")

        for element in doc_element.iter():
            if element.text and element.tag in {"p", "h", "q", "li", "ol", "ul"}:  # Ensure lists are included
                updated_text, id = update_fn(element.text)

                element.text = updated_text
                if id:
                    element.set("id", id)

        return document

    def add_warnings(self, document, warnings):
        """
        Add warnings to the document.
        """
        if not warnings:
            return  # No warnings, skip

        warnings_section = document.find("warnings")
        if warnings_section is None:
            warnings_section = etree.SubElement(document, "warnings")

        for id, warnings in warnings:
            for warning in warnings:
                warning_element = etree.SubElement(warnings_section, "warning")
                warning_element.text = warning
                warning_element.set("id", id)

    def add_errors(self, document, errors):
        """
        Add errors to the document.
        """
        if not errors:
            return  # No errors, skip

        errors_section = document.find("errors")
        if errors_section is None:
            errors_section = etree.SubElement(document, "errors")

        for id, errors in errors:
            for error in errors:
                error_element = etree.SubElement(errors_section, "error")
                error_element.text = error
                error_element.set("id", id)