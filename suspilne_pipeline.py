from sources.evaluator.language_tool_evaluator import LanguageToolEvaluator
from sources.tokenizer.custom_tokenizer import CustomTokenizer
from sources.utils.sanitize_and_transliterate import sanitize_and_transliterate
from sources.normalizer.news_normalizer import NewsNormalizer
from sources.saver.file_saver import FileSaver
from sources.annotator.xml_annotator import XMLAnnotator
from sources.source.suspilne_source import SuspilneSource
from sources.parser.suspilne_parser import SuspilneParser

if __name__ == "__main__":
    corpus_path = "corpus"
    with LanguageToolEvaluator() as evaluator:

        word_tokenizer = CustomTokenizer()
        sentence_tokenizer = CustomTokenizer(words=False)

        for record in SuspilneSource.records(mock=True):
            title = record.metadata.title
            safe_title = sanitize_and_transliterate(title)

            print(f"Processing: {title}")
            content = record.content()

            annotator = XMLAnnotator()
            document = SuspilneParser.parse(content, metadata=record.metadata, annotator=annotator)
            base_text = annotator.get_string(document)

            saver = FileSaver(path=f"{corpus_path}/base")
            saver.save(base_text, name=f"{safe_title}.txt")

            warnings = []
            errors = []

            counter = 1


            def normalize(text: str) -> (str, str):
                global counter

                new_text, new_warnings, new_errors = NewsNormalizer.normalize(text)

                if new_errors or new_warnings:
                    id = f"e{counter}"
                    counter += 1

                    warnings.append((id, new_warnings))
                    errors.append((id, new_errors))

                    return new_text, id

                return new_text, None


            document = annotator.update_elements(document, normalize)

            annotator.add_warnings(document, warnings)
            annotator.add_errors(document, errors)
            normalized_text = annotator.get_string(document)

            saver = FileSaver(path=f"{corpus_path}/normalized")
            saver.save(normalized_text, name=f"{safe_title}.txt")

            warnings = []
            errors = []


            def evaluate(text: str) -> (str, str):
                global counter
                new_warnings, new_errors = evaluator.evaluate(text)
                print("Warnings: ", len(new_warnings))
                print("Errors: ", len(new_warnings))
                if new_errors or new_warnings:
                    id = f"e{counter}"
                    counter += 1

                    warnings.append((id, new_warnings))
                    errors.append((id, new_errors))

                    return text, id

                return text, None


            document = annotator.update_elements(document, evaluate)

            annotator.add_warnings(document, warnings)
            annotator.add_errors(document, errors)
            evaluated_text = annotator.get_string(document)

            saver = FileSaver(path=f"{corpus_path}/evaluated")
            saver.save(evaluated_text, name=f"{safe_title}.txt")

            def split_s_fn(text: str) -> [str]:
                return sentence_tokenizer.tokenize(text)

            def split_w_fn(text: str) -> [str]:
                return word_tokenizer.tokenize(text)

            document = annotator.split_elements(document, split_s_fn, split_w_fn)
            tokenized_text = annotator.get_string(document)

            saver = FileSaver(path=f"{corpus_path}/tokenized")
            saver.save(tokenized_text, name=f"{safe_title}.txt")

            print(f"Finished: {title}")
