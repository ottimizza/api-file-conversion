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
       
        # inicialização das mandingas...
        self.pdf_file = pdf_file
        self.csv_file = self.pdf_file.replace(
            ".pdf", ".csv").replace(".PDF", ".csv")

        self.strategy = config.strategy()
        self.config = config

        # um dicionario contendo as celulas relacionadas a cada pagina numerada.
        # {
        #   1: [ cells... ]
        #   2: [ more cells... ]
        # }
        self.pages = {}
        self.cells = []  # deprecated

        print(len(self.pages))

    def parse(self):
        # Abre o arquivo PDF em modo de leitura binaria
        self.fp = open(self.pdf_file, 'rb')

        # Cria uma instancia do PDFParser associada ao arquivo.
        self.parser = PDFParser(self.fp)

        # cria uma instancia de PDFDocument contendo a estrutura do documento PDF.
        # ** SE PRECISAR DE SENHA É O SEGUNDO ARGUMENTO **
        self.document = PDFDocument(self.parser, self.config.password)

        # Verfica se o documento contém texto para extração. Se não, aborta.
        if not self.document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Cria uma instancia de PDFResourceManager contendo recursos compartilhados..
        self.resource_manager = PDFResourceManager()

        # Cria uma instancia de PDFDevice
        self.device = PDFDevice(self.resource_manager)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        self.laparams = LAParams(
            line_margin=0, char_margin=0.5, boxes_flow=-0.5)

        # Cria uma instancia de PDFPageAggregator
        self.device = PDFPageAggregator(
            self.resource_manager, laparams=self.laparams)

        # Cria uma instancia de PDFPageInterpreter
        self.interpreter = PDFPageInterpreter(
            self.resource_manager, self.device)

        # iteração das páginas do documento.
        for (index, page) in enumerate(PDFPage.create_pages(self.document)):

            # apenas as paginas informadas!
            if index not in self.config.pages():
                continue

            # faz a interpretação do PDF e retorna o layout do mesmo
            self.interpreter.process_page(page)
            layout = self.device.get_result()

            # utiliza a estratégia passada como parametro, para realizar
            # a extração das células de texto da página atual.

            parsed_cells = self.strategy.parse(layout, page, [])

            print("""
                Cells: {0}
            """.format(len(parsed_cells)))

            self.pages[index] = parsed_cells

            # *** **** **** ** * ** * ** * ** * **
            # ISSO AQUI TA BIZARRO
            #
            # após multiplas requisições... o numero aumenta
            #   req1 --> 266
            #   re12 --> 532
            #   ....
            #
            # *** **** **** ** * ** * ** * ** * **
            print(len(parsed_cells))

    def write(self, tempfile=None):

        opts = {
            "delimiter": self.config.delimiter()
        }

        if tempfile:
            self.csv_file = tempfile.name

        # faz a iteração das páginas processadas e constroi um CSV
        for page_index in self.pages.keys():
            csv_builder = CSVBuilder(**opts)

            cells = self.pages[page_index]  # self.cells

            csv_builder.build(cells)
            csv_builder.write(self.csv_file)

        return self.csv_file
