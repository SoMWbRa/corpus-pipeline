from abc import ABC, abstractmethod

from sources.utils.sanitize_and_transliterate import sanitize_and_transliterate


class AbstractPipeline(ABC):
    """
    Abstract base class for processing pipelines.
    Defines the full processing flow while subclasses provide specific components.
    """

    def __init__(self, output_path="corpus"):
        """
        Initialize the pipeline.
        """
        self.output_path = output_path
        self.source = self.get_source()
        self.annotator = self.get_annotator()
        self.parser = self.get_parser()
        self.normalizer = self.get_normalizer()
        self.evaluator = self.get_evaluator()
        self.corrector = self.get_corrector()
        self.word_tokenizer, self.sentence_tokenizer = self.get_tokenizers()

    def execute(self, start, end):
        """
        Execute the full pipeline over the specified time range.
        """
        try:

            with self.evaluator:
                for record in self.source.records(start=start, end=end):
                    self._process_record(record)
        except Exception as e:
            print(f"Pipeline execution error: {e}")

    def _process_record(self, record):
        """
        Process a single record through the pipeline.
        """
        title = record.metadata.title
        safe_title = sanitize_and_transliterate(title)
        print(f"Processing: {title}")

        self.warning_counter = 1
        self.error_counter = 1

        document = self._parse_document(record, safe_title)
        document = self._normalize_document(document, safe_title)
        document = self._evaluate_and_correct_document(document, safe_title)
        document = self._tokenize_document(document, safe_title)

        print(f"Finished: {title}")

    def _parse_document(self, record, safe_title):
        document = self.parser.parse(record.content(), metadata=record.metadata, annotator=self.annotator)
        base_text = self.annotator.get_string(document)
        self.get_saver(f"{self.output_path}/base").save(base_text, name=f"{safe_title}.txt")
        return document

    def _normalize_document(self, document, safe_title):
        document = self._apply_normalization(document)
        normalized_text = self.annotator.get_string(document)
        self.get_saver(f"{self.output_path}/normalized").save(normalized_text, name=f"{safe_title}.txt")
        return document

    def _evaluate_and_correct_document(self, document, safe_title):
        document = self._apply_evaluation_correction(document)
        evaluated_text = self.annotator.get_string(document)
        self.get_saver(f"{self.output_path}/evaluated").save(evaluated_text, name=f"{safe_title}.txt")
        return document

    def _tokenize_document(self, document, safe_title):
        document = self.annotator.split_elements(
            document,
            lambda text: self.sentence_tokenizer.tokenize(text),
            lambda text: self.word_tokenizer.tokenize(text)
        )
        tokenized_text = self.annotator.get_string(document)
        self.get_saver(f"{self.output_path}/tokenized").save(tokenized_text, name=f"{safe_title}.txt")
        return document

    def _apply_normalization(self, document):
        """
        Apply normalization to document.
        """
        warnings = []
        errors = []

        def normalize(text):
            new_text, new_warnings, new_errors = self.normalizer.normalize(text)

            ids = []
            for err in new_errors:
                e_id = f"e{self.error_counter}"
                self.error_counter += 1
                errors.append((e_id, err))
                ids.append(e_id)

            for warn in new_warnings:
                w_id = f"w{self.warning_counter}"
                self.warning_counter += 1
                warnings.append((w_id, warn))
                ids.append(w_id)

            return new_text, ", ".join(ids) if ids else None

        document = self.annotator.update_elements(document, normalize)
        self.annotator.add_warnings(document, warnings)
        self.annotator.add_errors(document, errors)

        return document

    def _apply_evaluation_correction(self, document):
        """
        Apply evaluation and correction to document.
        """
        warnings = []
        errors = []

        def evaluate_and_correct(text):

            # Initial evaluation
            new_warnings, new_errors = self.evaluator.evaluate(text)

            # Apply correction cycle
            max_iterations = 3
            iterations = 0
            current_text = text
            current_warnings = new_warnings
            current_errors = new_errors

            while iterations < max_iterations and (current_warnings or current_errors):
                corrected_text, remaining_warnings, remaining_errors = self.corrector.correct(
                    current_text, current_warnings, current_errors
                )

                if corrected_text == current_text or iterations == max_iterations - 1:
                    break

                current_text = corrected_text
                current_warnings, current_errors = self.evaluator.evaluate(current_text)
                iterations += 1

            ids = []
            for err in current_errors:
                e_id = f"e{self.error_counter}"
                self.error_counter += 1
                errors.append((e_id, err))
                ids.append(e_id)

            for warn in current_warnings:
                w_id = f"w{self.warning_counter}"
                self.warning_counter += 1
                warnings.append((w_id, warn))
                ids.append(w_id)

            return current_text, ", ".join(ids) if ids else None

        document = self.annotator.update_elements(document, evaluate_and_correct)
        self.annotator.add_warnings(document, warnings)
        self.annotator.add_errors(document, errors)

        return document

    @abstractmethod
    def get_source(self):
        pass

    @abstractmethod
    def get_annotator(self):
        pass

    @abstractmethod
    def get_parser(self):
        pass

    @abstractmethod
    def get_normalizer(self):
        pass

    @abstractmethod
    def get_evaluator(self):
        pass

    @abstractmethod
    def get_corrector(self):
        pass

    @abstractmethod
    def get_tokenizers(self):
        pass

    @abstractmethod
    def get_saver(self, path):
        pass
