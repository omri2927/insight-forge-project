import csv
import json
import chardet
import io

from .models import Document, DocumentProcessingResult

class DocumentParser:
    @staticmethod
    def _detect_encoding(document):
        with document.stored_file.open('rb') as f:
            raw_data = f.read(10240)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'

    @staticmethod
    def _base_parser(document: Document) -> DocumentProcessingResult:
        res, _ = DocumentProcessingResult.objects.get_or_create(document=document)

        res.parsing_status = DocumentProcessingResult.ParsingStatus.STARTING
        res.indexing_status = DocumentProcessingResult.IndexingStatus.WAITING
        res.detected_encoding = DocumentParser._detect_encoding(document=document)

        return res

    @staticmethod
    def _parse_text_file(document: Document) -> DocumentProcessingResult:
        res: DocumentProcessingResult = DocumentParser._base_parser(document=document)

        try:
            with document.stored_file.open('rb') as f_binary:
                f = io.TextIOWrapper(f_binary, encoding=res.detected_encoding, errors="ignore")

                res.row_count = sum(1 for line in f)
                res.column_count = 1

                res.summary = f"Text file parsed successfully with " \
                                             f"{res.row_count} lines"
            res.parsing_status = DocumentProcessingResult.ParsingStatus.SUCCESS
            res.error_message = None
        except Exception as e:
            res.parsing_status = DocumentProcessingResult.ParsingStatus.FAILED
            res.error_message = str(e)

        return res

    @staticmethod
    def _parse_csv_file(document: Document) -> DocumentProcessingResult:
        res: DocumentProcessingResult = DocumentParser._base_parser(document=document)

        try:
            with document.stored_file.open('rb') as f_binary:
                f = io.TextIOWrapper(f_binary, encoding=res.detected_encoding, errors="ignore")

                sample = f.read(2048)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample)
                has_header = csv.Sniffer().has_header(sample)
                reader = csv.reader(f, dialect=dialect)

                data = list(reader)
                rows = len(data) - 1 if has_header else len(data)
                cols = len(data[0]) if data else 0

                res.row_count = rows
                res.column_count = cols

                res.summary = f"CSV file parsed successfully with {res.row_count} rows " \
                                             f"and {res.column_count} columns"
                res.parsing_status = DocumentProcessingResult.ParsingStatus.SUCCESS
                res.error_message = None
        except Exception as e:
            res.parsing_status = DocumentProcessingResult.ParsingStatus.FAILED
            res.error_message = str(e)

        return res

    @staticmethod
    def _parse_json_file(document: Document) -> DocumentProcessingResult:
        res: DocumentProcessingResult = DocumentParser._base_parser(document=document)

        try:
            with document.stored_file.open('rb') as f_binary:
                f = io.TextIOWrapper(f_binary, encoding=res.detected_encoding, errors="ignore")

                data = json.load(f)
                if isinstance(data, list):
                    res.row_count = len(data)
                    res.column_count = len(data[0]) if data and isinstance(data[0], dict) else 1
                    res.summary = f"JSON file parsed successfully. Detected list of {res.row_count} items."
                elif isinstance(data, dict):
                    res.row_count = 1
                    res.column_count = len(data.keys())
                    res.summary = f"JSON file parsed successfully. Detected dictionary of {res.column_count} items."
                else:
                    res.row_count = 1
                    res.column_count = 1

                res.parsing_status = DocumentProcessingResult.ParsingStatus.SUCCESS
                res.error_message = None
        except Exception as e:
            res.error_message = str(e)
            res.parsing_status = DocumentProcessingResult.ParsingStatus.FAILED

        return res

    @staticmethod
    def _unsupported_format_parsing(document: Document) -> DocumentProcessingResult:
        res = DocumentParser._base_parser(document=document)

        res.parsing_status = DocumentProcessingResult.ParsingStatus.UNSUPPORTED_FORMAT
        res.error_message = "The format of the file you uploaded is unsupported right now in the system"

        return res

    @staticmethod
    def parse_document(document: Document) -> None:
            processing_result: DocumentProcessingResult = None
            ext = document.document_type.extension
            if ext == '.txt':
                processing_result = DocumentParser._parse_text_file(document=document)
            elif ext == '.csv':
                processing_result = DocumentParser._parse_csv_file(document=document)
            elif ext == '.json':
                processing_result = DocumentParser._parse_json_file(document=document)
            else:
                processing_result = DocumentParser._unsupported_format_parsing(document=document)

            processing_result.save()
