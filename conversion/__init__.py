
# class CSVDelimiter:
#     """
#     Default CSV file delimiters.
#     """
#     COMMA, PIPE, SEMICOLON = ",", "|", ";"


# class PDFParserConfig:

#     def __init__(self, **kwargs):
#         self.delimiter = kwargs.get("delimiter", CSVDelimiter.SEMICOLON)
#         self.password = kwargs.get("password", None)
#         self.pages = self._standardize_pages(kwargs.get("pages", "[0-50]"))
#         self.trim = kwargs.get("trim", True)
#         self.shrink = kwargs.get("shrink", False)
#         self.laparams = kwargs.get("laparams", {})

#     def _has_interval(self, interval):
#         return len(interval.split('-')) > 1

#     def _get_interval(self, interval):
#         return tuple(map(int, interval.split('-')))

#     def _standardize_pages(self, _pages):
#         pages = []
#         _pages = _pages.replace(' ', '')
#         if _pages.startswith("[") and _pages.endswith("]"):
#             intervals = _pages.replace("[", "").replace("]", "").split(",")
#             for interval in intervals:
#                 if self._has_interval(interval):
#                     (i0, i1) = self._get_interval(interval)
#                     for i in range(i0, i1+1):
#                         pages.append(i)
#                 else:
#                     (i0,) = self._get_interval(interval)
#                     pages.append(i0)
#             pages.sort()
#         return pages


# class PDFParser:

#     def __init__(self, config: PDFParserConfig):
#         pass


# from conversion.strategy import ParseStrategyA
from conversion.builder import CSVBuilder

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

class PDFConverterConfig:

    DELIMITER_PIPE = "|"
    DELIMITER_COMMA = ","
    DELIMITER_SEMICOLON = ";"

    def __init__(self, **kwargs):
        """
        """
        self._strategy = kwargs.get("strategy")
        self._delimiter = kwargs.get("delimiter", PDFConverterConfig.DELIMITER_SEMICOLON)
        self._password = kwargs.get("password", None)
        self._pages = self.standardize_pages(kwargs.get("pages", "[0-50]"))
        self._trim = kwargs.get("trim", True)
        self._shrink = kwargs.get("shrink", False)

        self._la_char_margin = kwargs.get("char_margin", None)
        self._la_line_margin = kwargs.get("line_margin", None)
        self._la_word_margin = kwargs.get("word_margin", None)

    def has_interval(self, interval):
        return len(interval.split('-')) > 1

    def get_interval(self, interval):
        return tuple(map(int, interval.split('-')))

    def standardize_pages(self, _pages):
        pages = []
        _pages = _pages.replace(' ', '')
        if _pages.startswith("[") and _pages.endswith("]"):
            intervals = _pages.replace("[", "").replace("]", "").split(",")
            for interval in intervals:
                if self.has_interval(interval):
                    (i0, i1) = self.get_interval(interval)
                    for i in range(i0, i1+1):
                        pages.append(i)
                else:
                    (i0,) = self.get_interval(interval)
                    pages.append(i0)
            pages.sort()
        return pages

    def delimiter(self):
        return self._delimiter

    def pages(self):
        return self._pages

    def password(self):
        return self._password


class PDFConverter:

    def __init__(self, pdf_file, strategy, config):
        self.pdf_file = pdf_file

        self.strategy = strategy
        self.config = config

        self.cells = []
        
    @property
    def current_page(self):
        return self._current_page
    
    @current_page.setter
    def current_page(self, current_page):
        self._current_page = current_page

    def parse(self):
        # Open the PDF File.
        self.fp = open(self.pdf_file, 'rb')

        # Create a PDF parser object associated with the file object.
        self.parser = PDFParser(self.fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        self.document = PDFDocument(self.parser, self.config.password)

        # Check if the document allows text extraction. If not, abort.
        if not self.document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        self.resource_manager = PDFResourceManager()

        # Create a PDF device object.
        self.device = PDFDevice(self.resource_manager)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        self.laparams = LAParams(line_margin=0, char_margin=0.5, boxes_flow=-0.5)

        # Create a PDF page aggregator object.
        self.device = PDFPageAggregator(self.resource_manager, laparams=self.laparams)

        # Create a PDF interpreter object.
        self.interpreter = PDFPageInterpreter(self.resource_manager, self.device)

        # loop over all pages in the document
        for (index, page) in enumerate(PDFPage.create_pages(self.document)):

            if index not in self.config.pages():
                continue

            self.current_page = page

            # read the page into a` layout object
            self.interpreter.process_page(page)
            layout = self.device.get_result()

            self.cells = self.strategy.parse(layout, page)

        return self


    def write(self):
        outpath = self.pdf_file.replace(".pdf", ".csv").replace(".PDF", ".csv")
        csv_builder = CSVBuilder()
        csv_builder.build(self.cells)
        csv_builder.write(outpath)

        return outpath


# parser = PDFParser(pdf_file, parse_strategy, parse_config)






