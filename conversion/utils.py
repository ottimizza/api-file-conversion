def trim(text):
    import re
    # remove espaços duplos
    text = re.sub("[^\S\r\n]{2,}", " ", text)
    
    # remove espaços antes e depois da string
    text = re.sub("^[^\S\r\n]", "", text)
    text = re.sub("[^\S\r\n]$", "", text)
    
    return text


class CustomArrayParser:

    @classmethod
    def has_interval(cls, interval):
        return len(interval.split('-')) > 1

    @classmethod
    def get_interval(cls, interval):
        return tuple(map(int, interval.split('-')))

    @classmethod
    def parse(cls, _pages: str):
        pages = []
        _pages = _pages.replace(' ', '')
        if _pages.startswith("[") and _pages.endswith("]"):
            intervals = _pages.replace("[", "").replace("]", "").split(",")
            for interval in intervals:
                if cls.has_interval(interval):
                    (i0, i1) = CustomArrayParser.get_interval(interval)
                    for i in range(i0, i1+1):
                        pages.append(i)
                else:
                    (i0,) = cls.get_interval(interval)
                    pages.append(i0)
            pages.sort()
        return pages
