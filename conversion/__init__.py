
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
from conversion.config import PDFConverterConfig
from conversion.utils import CustomArrayParser

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

class PDFConverter:

    def __init__(self, pdf_file, config: PDFConverterConfig):
        self.pdf_file = pdf_file
        self.csv_file = self.pdf_file.replace(".pdf", ".csv").replace(".PDF", ".csv")

        self.strategy = config.strategy()
        self.config = config

        # um dicionario contendo as celulas relacionadas a cada pagina numerada
        self.pages = {}
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

            self.pages[index] = self.strategy.parse(layout, page)

            # self.cells = self.strategy.parse(layout, page)

        return self


    def write(self):

        opts = {
            "delimiter": self.config.delimiter()
        }

        for page_index in self.pages.keys():
            csv_builder = CSVBuilder(**opts)

            cells = self.pages[page_index] # self.cells

            csv_builder.build(cells)
            csv_builder.write(self.csv_file)

        return self.csv_file


# parser = PDFParser(pdf_file, parse_strategy, parse_config)






