from sources.tokenizer.abstract_tokenizer import AbstractTokenizer
import csv
import re
import spacy
from spacy.util import filter_spans
import os

from spacy.lang.char_classes import (
    ALPHA,
    ALPHA_LOWER,
    ALPHA_UPPER,
    COMBINING_DIACRITICS,
    CONCAT_QUOTES,
    CURRENCY,
    HYPHENS,
    LIST_CURRENCY,
    LIST_ELLIPSES,
    LIST_ICONS,
    LIST_PUNCT,
    LIST_QUOTES,
    PUNCT,
    UNITS,
    merge_chars,
)
from spacy.symbols import ORTH, NORM


class CustomTokenizer(AbstractTokenizer):
    # Removed °, № from _other_symbols
    custom_other_symbols = (
        r"\u00A6\u00A9\u00AE\u0482\u058D\u058E\u060E\u060F\u06DE\u06E9\u06FD\u06FE\u07F6\u09FA\u0B70"
        r"\u0BF3-\u0BF8\u0BFA\u0C7F\u0D4F\u0D79\u0F01-\u0F03\u0F13\u0F15-\u0F17\u0F1A-\u0F1F\u0F34"
        r"\u0F36\u0F38\u0FBE-\u0FC5\u0FC7-\u0FCC\u0FCE\u0FCF\u0FD5-\u0FD8\u109E\u109F\u1390-\u1399"
        r"\u1940\u19DE-\u19FF\u1B61-\u1B6A\u1B74-\u1B7C\u2100\u2101\u2103-\u2106\u2108\u2109\u2114"
        r"\u2117\u211E-\u2123\u2125\u2127\u2129\u212E\u213A\u213B\u214A\u214C\u214D\u214F\u218A\u218B"
        r"\u2195-\u2199\u219C-\u219F\u21A1\u21A2\u21A4\u21A5\u21A7-\u21AD\u21AF-\u21CD\u21D0\u21D1\u21D3"
        r"\u21D5-\u21F3\u2300-\u2307\u230C-\u231F\u2322-\u2328\u232B-\u237B\u237D-\u239A\u23B4-\u23DB"
        r"\u23E2-\u2426\u2440-\u244A\u249C-\u24E9\u2500-\u25B6\u25B8-\u25C0\u25C2-\u25F7\u2600-\u266E"
        r"\u2670-\u2767\u2794-\u27BF\u2800-\u28FF\u2B00-\u2B2F\u2B45\u2B46\u2B4D-\u2B73\u2B76-\u2B95"
        r"\u2B98-\u2BC8\u2BCA-\u2BFE\u2CE5-\u2CEA\u2E80-\u2E99\u2E9B-\u2EF3\u2F00-\u2FD5\u2FF0-\u2FFB"
        r"\u3004\u3012\u3013\u3020\u3036\u3037\u303E\u303F\u3190\u3191\u3196-\u319F\u31C0-\u31E3"
        r"\u3200-\u321E\u322A-\u3247\u3250\u3260-\u327F\u328A-\u32B0\u32C0-\u32FE\u3300-\u33FF\u4DC0-\u4DFF"
        r"\uA490-\uA4C6\uA828-\uA82B\uA836\uA837\uA839\uAA77-\uAA79\uFDFD\uFFE4\uFFE8\uFFED\uFFEE\uFFFC"
        r"\uFFFD\U00010137-\U0001013F\U00010179-\U00010189\U0001018C-\U0001018E\U00010190-\U0001019B"
        r"\U000101A0\U000101D0-\U000101FC\U00010877\U00010878\U00010AC8\U0001173F\U00016B3C-\U00016B3F"
        r"\U00016B45\U0001BC9C\U0001D000-\U0001D0F5\U0001D100-\U0001D126\U0001D129-\U0001D164"
        r"\U0001D16A-\U0001D16C\U0001D183\U0001D184\U0001D18C-\U0001D1A9\U0001D1AE-\U0001D1E8"
        r"\U0001D200-\U0001D241\U0001D245\U0001D300-\U0001D356\U0001D800-\U0001D9FF\U0001DA37-\U0001DA3A"
        r"\U0001DA6D-\U0001DA74\U0001DA76-\U0001DA83\U0001DA85\U0001DA86\U0001ECAC\U0001F000-\U0001F02B"
        r"\U0001F030-\U0001F093\U0001F0A0-\U0001F0AE\U0001F0B1-\U0001F0BF\U0001F0C1-\U0001F0CF"
        r"\U0001F0D1-\U0001F0F5\U0001F110-\U0001F16B\U0001F170-\U0001F1AC\U0001F1E6-\U0001F202"
        r"\U0001F210-\U0001F23B\U0001F240-\U0001F248\U0001F250\U0001F251\U0001F260-\U0001F265"
        r"\U0001F300-\U0001F3FA\U0001F400-\U0001F6D4\U0001F6E0-\U0001F6EC\U0001F6F0-\U0001F6F9"
        r"\U0001F700-\U0001F773\U0001F780-\U0001F7D8\U0001F800-\U0001F80B\U0001F810-\U0001F847"
        r"\U0001F850-\U0001F859\U0001F860-\U0001F887\U0001F890-\U0001F8AD\U0001F900-\U0001F90B"
        r"\U0001F910-\U0001F93E\U0001F940-\U0001F970\U0001F973-\U0001F976\U0001F97A\U0001F97C-\U0001F9A2"
        r"\U0001F9B0-\U0001F9B9\U0001F9C0-\U0001F9C2\U0001F9D0-\U0001F9FF\U0001FA60-\U0001FA6D"
    )

    CUSTOM_LIST_ICONS = [r"[{i}]".format(i=custom_other_symbols)]

    TOKENIZER_PREFIXES = (
            ["§", "%", "=", "—", "–", r"\+(?![0-9])"]
            + LIST_PUNCT
            + LIST_ELLIPSES
            + LIST_QUOTES
            # + LIST_CURRENCY # added support for currency
            + CUSTOM_LIST_ICONS
    )

    TOKENIZER_SUFFIXES = (
            LIST_PUNCT
            + LIST_ELLIPSES
            + LIST_QUOTES
            + CUSTOM_LIST_ICONS
            + ["'s", "'S", "’s", "’S", "—", "–"]
            + [
                r"(?<=[0-9])\+",

                # r"(?<=°[FfCcKk])\.", # replaced with the next line
                r"(?<=°)\.|(?<=°[FfCcKk])\.",  # dot breakdown for °. pattern

                # r"(?<=[0-9])(?:{c})".format(c=CURRENCY), # added support for currency
                # r"(?<=[0-9])(?:{u})".format(u=UNITS), # added support for units
                r"(?<=[0-9{al}{e}{p}(?:{q})])\.".format(
                    al=ALPHA_LOWER, e=r"%²\-\+", q=CONCAT_QUOTES, p=PUNCT
                ),
                r"(?<=[{au}][{au}])\.".format(au=ALPHA_UPPER),
            ]
    )

    # Removed - from _hyphens
    custom_hyphens = "– — -- --- —— ~"
    HYPHENS_CUSTOM = merge_chars(custom_hyphens)

    TOKENIZER_INFIXES = (
            LIST_ELLIPSES
            + CUSTOM_LIST_ICONS
            + [

                # r"(?<=[0-9])[+\-\*^](?=[0-9-])", # replaced with the next two lines. added HYPHENS support between number
                r"(?<=[0-9])[+*^](?=[0-9-])",
                r"(?<=[0-9])-(?=-)",

                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                ),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS_CUSTOM),
                # r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA), # replaced with the next line. Removed \
                r"(?<=[{a}0-9])[:<>=](?=[{a}])".format(a=ALPHA),
            ]
    )

    COMBINING_DIACRITICS_TOKENIZER_SUFFIXES = list(TOKENIZER_SUFFIXES) + [
        r"(?<=[{a}][{d}])\.".format(a=ALPHA, d=COMBINING_DIACRITICS),
    ]

    COMBINING_DIACRITICS_TOKENIZER_INFIXES = list(TOKENIZER_INFIXES) + [
        r"(?<=[{al}][{d}])\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES, d=COMBINING_DIACRITICS
        ),
        r"(?<=[{a}][{d}]),(?=[{a}])".format(a=ALPHA, d=COMBINING_DIACRITICS),
        r"(?<=[{a}][{d}])(?:{h})(?=[{a}])".format(
            a=ALPHA, d=COMBINING_DIACRITICS, h=HYPHENS_CUSTOM
        ),
        r"(?<=[{a}][{d}])[:<>=/](?=[{a}])".format(a=ALPHA, d=COMBINING_DIACRITICS),
    ]

    phone_pattern = re.compile(r"\+?\b(?:\d{1,3})?0?[\s-]?\(?\d{2,3}\)?[\s-]?\d{2,3}[\s-]?\d{2,3}[\s-]?\d{2,3}\b")

    number_pattern = re.compile(r"(?<!\d)\b\d{1,3}(?: \d{3})+\b(?! \d)")

    prefix_regex = spacy.util.compile_prefix_regex(TOKENIZER_PREFIXES)
    suffix_regex = spacy.util.compile_suffix_regex(COMBINING_DIACRITICS_TOKENIZER_SUFFIXES)
    infix_regex = spacy.util.compile_infix_regex(COMBINING_DIACRITICS_TOKENIZER_INFIXES)

    def __init__(self):

        # Download model if not already downloaded
        try:
            spacy.load("uk_core_news_sm")
        except OSError:
            os.system("python -m spacy download uk_core_news_sm")

        self.nlp = spacy.load("uk_core_news_sm", enable=["parser"])
        self.EXCEPTIONS_WITH_SPACES = []
        self.EXCEPTIONS = []
        self.nlp.tokenizer = self.setup_tokenizer(self.nlp)

    def name(self) -> str:
        return "Custom Tokenizer"

    def tokenize(self, text: str, words: bool = True) -> list:
        doc = self.nlp(text)
        self.retokenize(doc, text)

        if words:
            return [token.text for token in doc]
        else:
            return [sent.text for sent in doc.sents]

    def setup_tokenizer(self, nlp):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        csv_path = os.path.join(project_root, 'data', 'abbreviations.csv')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                orth = row['abbreviation']
                norm = row['definition']
                self.EXCEPTIONS.append({ORTH: orth, NORM: norm})
                if ' ' in orth:
                    self.EXCEPTIONS_WITH_SPACES.append(orth)

        tokenizer = nlp.tokenizer

        tokenizer.prefix_search = self.prefix_regex.search
        tokenizer.suffix_search = self.suffix_regex.search
        tokenizer.infix_finditer = self.infix_regex.finditer

        for token_exception in self.EXCEPTIONS:
            tokenizer.add_special_case(token_exception[ORTH], [token_exception])

        return tokenizer

    def retokenize(self, doc, text):
        spans = []

        for pattern in [self.phone_pattern, self.number_pattern]:
            for match in pattern.finditer(text):
                start, end = match.span()
                span = doc.char_span(start, end, alignment_mode="expand")
                if span is not None:
                    spans.append(span)

        # If added three exceptions: "a. b.", "a." and "b.".
        # Then "a. b." will still be broken down. So we merge tokens for these
        for phrase in self.EXCEPTIONS_WITH_SPACES:
            start = text.find(phrase)
            if start != -1:
                end = start + len(phrase)
                span = doc.char_span(start, end, alignment_mode="expand")
                if span is not None:
                    spans.append(span)

        filtered_spans = filter_spans(spans)

        with doc.retokenize() as retokenizer:
            for span in filtered_spans:
                retokenizer.merge(span)

        return doc


if __name__ == "__main__":
    tokenizer = CustomTokenizer()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    raw_text_file = os.path.join(project_root, 'data', 'text_raw.txt')
    tokenized_file = os.path.join(project_root, 'data', 'text_tokenized.txt')

    with open(raw_text_file, "r", encoding="utf-8") as file:
        raw_text_list = file.read().split("\n")
        raw_text = " ".join(raw_text_list)

    with open(tokenized_file, "r", encoding="utf-8") as file:
        expected_tokens = [line.strip() for line in file]

    actual_tokens = tokenizer.tokenize(raw_text)

    assert actual_tokens == expected_tokens, "Tokenization failed"
    print("Tokenization successful")