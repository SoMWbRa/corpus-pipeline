from sources.pipeline.abstract_pipeline import AbstractPipeline
from sources.corrector.no_changes_corrector import NoChangesCorrector
from sources.evaluator.language_tool_evaluator import LanguageToolEvaluator
from sources.tokenizer.custom_tokenizer import CustomTokenizer
from sources.normalizer.news_normalizer import NewsNormalizer
from sources.saver.file_saver import FileSaver
from sources.annotator.xml_annotator import XMLAnnotator
from sources.source.suspilne_source import SuspilneSource
from sources.parser.suspilne_parser import SuspilneParser


class SuspilnePipeline(AbstractPipeline):
    """
    Pipeline implementation for processing Suspilne news.
    """

    def get_source(self):
        return SuspilneSource()

    def get_annotator(self):
        return XMLAnnotator()

    def get_parser(self):
        return SuspilneParser()

    def get_normalizer(self):
        return NewsNormalizer()

    def get_evaluator(self):
        return LanguageToolEvaluator()

    def get_corrector(self):
        return NoChangesCorrector()

    def get_tokenizers(self):
        return CustomTokenizer(), CustomTokenizer(words=False)

    def get_saver(self, path):
        return FileSaver(path=path)
