
class CSVDelimiter:
    """
    Default CSV file delimiters.
    """
    COMMA, PIPE, SEMICOLON = ",", "|", ";"


class PDFParserConfig:

    def __init__(self, **kwargs):
        self.delimiter = kwargs.get("delimiter", CSVDelimiter.SEMICOLON)
        self.password = kwargs.get("password", None)
        self.pages = self._standardize_pages(kwargs.get("pages", "[0-50]"))
        self.trim = kwargs.get("trim", True)
        self.shrink = kwargs.get("shrink", False)
        self.laparams = kwargs.get("laparams", {})

    def _has_interval(self, interval):
        return len(interval.split('-')) > 1

    def _get_interval(self, interval):
        return tuple(map(int, interval.split('-')))

    def _standardize_pages(self, _pages):
        pages = []
        _pages = _pages.replace(' ', '')
        if _pages.startswith("[") and _pages.endswith("]"):
            intervals = _pages.replace("[", "").replace("]", "").split(",")
            for interval in intervals:
                if self._has_interval(interval):
                    (i0, i1) = self._get_interval(interval)
                    for i in range(i0, i1+1):
                        pages.append(i)
                else:
                    (i0,) = self._get_interval(interval)
                    pages.append(i0)
            pages.sort()
        return pages


class PDFParser:

    def __init__(self, config: PDFParserConfig):
        pass
