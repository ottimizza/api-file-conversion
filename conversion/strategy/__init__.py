from abc import ABC, abstractmethod

from conversion import PDFConverter
from conversion.models import Cell, Coordinate

import pdfminer

class ParseStrategy(ABC):

    @abstractmethod
    def parse(self, layout, pdf_converter_object: PDFConverter):
        pass


class ParseStrategyA(ParseStrategy):

    def get_coordinates(self, layout, page):
        (width, height) = (page.mediabox[2], page.mediabox[3])

        (x1, _y1, x2, _y2) = (layout.bbox[0], layout.bbox[1], layout.bbox[2], layout.bbox[3])

        y1 = height - _y1
        y2 = height - _y2

        return (x1, y1, x2, y2)

    def build_cell(self, layout_object, bbox):
        print(layout_object.get_text())
        content = layout_object.get_text().replace('\n', '')
        coordinates = Coordinate.from_bbox(bbox)
        return Cell('', content, coordinates)

    def parse(self, layout, page, cells = []):
        (width, height) = (page.mediabox[2], page.mediabox[3])

        for layout_object in layout:
            if isinstance(layout_object, pdfminer.layout.LTTextLine):
                (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)

                cell = self.build_cell(layout_object, (x1, y1, x2, y2))

                cells.append(cell)

            # if it's a textbox, recurse for text lines
            if isinstance(layout_object, pdfminer.layout.LTTextBoxHorizontal):
               self.parse(layout_object._objs, page, cells)
            
            # if it's a container, recurse
            elif isinstance(layout_object, pdfminer.layout.LTFigure):
                self.parse(layout_object._objs, page, cells)

        return cells


class ParseStrategyB(ParseStrategy):

    def get_coordinates(self, layout, page):
        (width, height) = (page.mediabox[2], page.mediabox[3])

        (x1, _y1, x2, _y2) = (layout.bbox[0], layout.bbox[1], layout.bbox[2], layout.bbox[3])

        y1 = height - _y1
        y2 = height - _y2

        return (x1, y1, x2, y2)

    def build_cell(self, layout_object, bbox):
        content = layout_object.get_text().replace('\n', ' ')
        coordinates = Coordinate.from_bbox(bbox)
        return Cell('', content, coordinates)

    def parse(self, layout, pdf_converter_object: PDFConverter):
        page = pdf_converter_object.current_page

        (width, height) = (page.mediabox[2], page.mediabox[3])

        for layout_object in layout:
            if isinstance(layout_object, pdfminer.layout.LTTextBoxHorizontal):
                (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)

                cell = self.build_cell(layout_object, (x1, y1, x2, y2))

                pdf_converter_object.cells.append(cell)

            # if it's a container, recurse
            elif isinstance(layout_object, pdfminer.layout.LTFigure):
                self.parse(layout_object._objs, pdf_converter_object)

        return pdf_converter_object.cells


class ParseStrategyC(ParseStrategy):

    def get_coordinates(self, layout, page):
        (width, height) = (page.mediabox[2], page.mediabox[3])

        (x1, _y1, x2, _y2) = (layout.bbox[0], layout.bbox[1], layout.bbox[2], layout.bbox[3])

        y1 = height - _y1
        y2 = height - _y2

        return (x1, y1, x2, y2)

    def build_cell(self, layout_object, bbox):
        content = layout_object.get_text().replace('\n', ';')
        coordinates = Coordinate.from_bbox(bbox)
        return Cell('', content, coordinates)

    def parse(self, layout, pdf_converter_object: PDFConverter):
        page = pdf_converter_object.current_page

        (width, height) = (page.mediabox[2], page.mediabox[3])

        for layout_object in layout:
            if isinstance(layout_object, pdfminer.layout.LTTextBoxHorizontal):
                (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)

                cell = self.build_cell(layout_object, (x1, y1, x2, y2))

                pdf_converter_object.cells.append(cell)

            # if it's a container, recurse
            elif isinstance(layout_object, pdfminer.layout.LTFigure):
                self.parse(layout_object._objs, pdf_converter_object)

        return pdf_converter_object.cells


class ParseStrategyD(ParseStrategy):

    def get_coordinates(self, layout, page):
        (width, height) = (page.mediabox[2], page.mediabox[3])

        (x1, _y1, x2, _y2) = (layout.bbox[0], layout.bbox[1], layout.bbox[2], layout.bbox[3])

        y1 = height - _y1
        y2 = height - _y2

        return (x1, y1, x2, y2)

    def build_cell(self, layout_object, bbox):
        content = layout_object.get_text().replace('\n', '')
        coordinates = Coordinate.from_bbox(bbox)
        return Cell('', content, coordinates)

    def parse(self, layout, pdf_converter_object: PDFConverter):
        page = pdf_converter_object.current_page

        (width, height) = (page.mediabox[2], page.mediabox[3])

        for layout_object in layout:
            LN = ""
            if isinstance(layout_object, pdfminer.layout.LTTextBox):
                print("--------------------    LTTextBox    ---------------------")
                box_cell = self.build_cell(layout_object, self.get_coordinates(layout_object, page))
                print(LN, "LTTextBox ...: ", box_cell)
                print(layout_object.get_text())
            
                LN = "\t"
                print("---------------------------------------------------------")
                for child_layout in layout_object._objs:
                    # print(LN, child_layout.__class__.__name__)
                    if isinstance(child_layout, pdfminer.layout.LTTextLine):
                        line_cell = self.build_cell(layout_object, self.get_coordinates(child_layout, page))
                        print(LN, "LTTextLine ...: ", line_cell)
                        print(LN, child_layout.get_text())


            # if isinstance(layout_object, pdfminer.layout.LTTextBoxHorizontal):
            #     # print("TH")
            #     (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)
            #     cell = self.build_cell(layout_object, (x1, y1, x2, y2))
            #     print(cell, cell.content)

            # if isinstance(layout_object, pdfminer.layout.LTTextBoxVertical):
            #     print("TV")
            #     (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)
            #     cell = self.build_cell(layout_object, (x1, y1, x2, y2))
            #     print(cell, cell.content)

            # if isinstance(layout_object, pdfminer.layout.LTTextLine):
            #     (x1, y1, x2, y2) = self.get_coordinates(layout_object, page)
            #     x1, x2 = self.x1, self.x2
                
            #     print(x1, y1, x2, y2)

            #     cell = self.build_cell(layout_object, (x1, y1, x2, y2))

            #     pdf_converter_object.cells.append(cell)

            # # if it's a textbox, recurse for text lines
            # if isinstance(layout_object, pdfminer.layout.LTTextBoxHorizontal):
            #     (self.x1, y1, self.x2, y2) = self.get_coordinates(layout_object, page)
            #     self.parse(layout_object._objs, pdf_converter_object)
            
            # if it's a container, recurse
            elif isinstance(layout_object, pdfminer.layout.LTFigure):
                self.parse(layout_object._objs, pdf_converter_object)

        return pdf_converter_object.cells
