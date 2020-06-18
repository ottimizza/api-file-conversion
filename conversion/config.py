from conversion.strategy import ParseStrategy, ParseStrategyA, ParseStrategyB, ParseStrategyC
from conversion.utils import CustomArrayParser

class PDFConverterConfig:

    DEFAULT_DELIMITER = ";"
    DEFAULT_STRATEGY = "LTTextLine"

    ## 1. LTTextLine
    ## 2. LTTextBox_UC
    ## 3. LTTextBox_MC

    DELIMITER_PIPE = "|"
    DELIMITER_COMMA = ","
    DELIMITER_SEMICOLON = ";"

    def __init__(self, **kwargs):
        """
        """
        self._strategy = kwargs.get("strategy", PDFConverterConfig.DEFAULT_STRATEGY)
        self._delimiter = kwargs.get("delimiter", PDFConverterConfig.DEFAULT_DELIMITER)
        self._password = kwargs.get("password", None)
        self._pages = CustomArrayParser.parse(kwargs.get("pages", "[0-50]"))
        self._trim = kwargs.get("trim", True)
        self._shrink = kwargs.get("shrink", False)

        self._la_char_margin = kwargs.get("char_margin", None)
        self._la_line_margin = kwargs.get("line_margin", None)
        self._la_word_margin = kwargs.get("word_margin", None)


    def strategy(self):
        switcher = {
            "LTTextLine": ParseStrategyA(),
            "LTTextBoxUC": ParseStrategyB(), # B
            "LTTextBoxMC": ParseStrategyC(), # C
        }  
        return switcher.get(self._strategy, ParseStrategyA())

    def delimiter(self):
        return self._delimiter

    def pages(self):
        return self._pages

    def password(self):
        return self._password

    def trim(self):
        return self._trim

    def shrink(self):
        return self._shrink

    @classmethod
    def default_opts(cls):
        return {
            "strategy": "LTTextLine",
            "delimiter": ";",
            "pages": "[0-5]",
            "password": None,
            "trim": True,
            "shrink": False
        }