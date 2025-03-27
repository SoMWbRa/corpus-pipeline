from bs4 import BeautifulSoup, Tag, NavigableString
from typing import Any
import html
import re

from sources.annotator.abstract_annotator import AbstractAnnotator
from sources.record.abstract_record import Metadata


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
            raise ValueError("Failed to find main content container in the HTML")

        document = annotator.create_document(metadata=metadata)

        SuspilneParser._process_content_elements(content_container, annotator, document)

        return document

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean text by:
        1. Unescaping HTML entities
        2. Fixing space issues
        3. Handling email address obfuscation

        Args:
            text: The text to clean

        Returns:
            Cleaned text
        """
        text = html.unescape(text)

        # Replace obfuscated email addresses with proper format
        # This is a simple example - might need to be enhanced for specific patterns
        text = re.sub(r'\[email&#160;protected\]', r'protected@mail.com', text)
        text = re.sub(r'\[email\s*?protected\]', r'protected@mail.com', text)

        return text.strip()

    @staticmethod
    def _process_content_elements(container: Tag, annotator: Any, document: Any) -> None:
        """
        Process content elements from the HTML and add them to the document.

        Args:
            container: BeautifulSoup Tag containing the content elements
            annotator: Annotator to use for document creation
            document: Document to add elements to
        """

        for explainer_popup in container.select("span.c-explainer__popup"):
            explainer_popup.decompose()

        for explainer_word in container.select("span.c-explainer__word"):
            explainer_word.unwrap()

        # First, decode any Cloudflare protected emails in the container
        SuspilneParser._decode_cloudflare_emails(container)

        for element in container.children:
            # Skip non-tag elements like NavigableString
            if not isinstance(element, Tag):
                continue

            tag_name = element.name

            # Process different types of content elements
            if tag_name and tag_name.startswith('h') and len(tag_name) == 2:
                # Heading elements (h1, h2, h3, etc.)
                text = SuspilneParser._extract_text_with_spacing(element)
                cleaned_text = SuspilneParser._clean_text(text)
                annotator.add_heading(document, SuspilneParser._clean_text(cleaned_text))

            elif tag_name == 'p':
                # Paragraph elements
                text = SuspilneParser._extract_text_with_spacing(element)
                cleaned_text = SuspilneParser._clean_text(text)
                if cleaned_text:  # Only add non-empty paragraphs
                    annotator.add_paragraph(document, cleaned_text)

            elif tag_name == 'ul':
                # Unordered list elements
                items = [SuspilneParser._clean_text(SuspilneParser._extract_text_with_spacing(li))
                         for li in element.find_all('li', recursive=False)]
                items = [item for item in items if item]  # Filter out empty items
                if items:  # Only add non-empty lists
                    annotator.add_list(document, items, ordered=False)

            elif tag_name == 'ol':
                # Ordered list elements
                items = [SuspilneParser._clean_text(SuspilneParser._extract_text_with_spacing(li))
                         for li in element.find_all('li', recursive=False)]
                items = [item for item in items if item]  # Filter out empty items
                if items:  # Only add non-empty lists
                    annotator.add_list(document, items, ordered=True)

            elif tag_name == 'blockquote':
                # Quote elements
                text = SuspilneParser._extract_text_with_spacing(element)
                annotator.add_quote(document, SuspilneParser._clean_text(text))

            elif tag_name == 'div':
                # Process div elements recursively if they might contain content
                if 'class' in element.attrs and any(
                        c in element.attrs['class'] for c in ['content-block', 'article-paragraph']):
                    SuspilneParser._process_content_elements(element, annotator, document)
                # Also process divs that contain other content elements
                elif element.find(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'blockquote']):
                    SuspilneParser._process_content_elements(element, annotator, document)

    @staticmethod
    def _decode_cloudflare_emails(container: Tag) -> None:
        """
        Find and decode Cloudflare-protected email addresses in the HTML.
        Replaces the obfuscated elements with the decoded email address.

        Args:
            container: BeautifulSoup Tag containing the content
        """
        # Find all Cloudflare protected email links
        cf_emails = container.find_all('a', class_='__cf_email__')

        for email_tag in cf_emails:
            if 'data-cfemail' in email_tag.attrs:
                encoded_email = email_tag['data-cfemail']
                try:
                    decoded_email = SuspilneParser._decode_email(encoded_email)
                    # Replace the [email protected] text with the actual email
                    email_tag.replace_with(decoded_email)
                except Exception as e:
                    print(f"Error decoding Cloudflare email: {e}")

    @staticmethod
    def _decode_email(e):
        """
        Decode an email address that has been encoded with Cloudflare's protection.

        Args:
            e: The hex string representing the encoded email

        Returns:
            Decoded email address
        """
        de = ""
        k = int(e[:2], 16)

        for i in range(2, len(e), 2):
            de += chr(int(e[i:i+2], 16) ^ k)

        return de

    @staticmethod
    def _extract_text_with_spacing(element: Tag) -> str:
        """
        Extract text from a BeautifulSoup element with proper spacing.
        This method preserves spaces between elements.

        Args:
            element: BeautifulSoup Tag to extract text from

        Returns:
            Extracted text with proper spacing
        """
        result = []
        for child in element.descendants:
            if isinstance(child, NavigableString):
                result.append(str(child))
            elif child.name in ['br', 'p', 'div', 'li']:
                result.append(' ')

        return ''.join(result)
