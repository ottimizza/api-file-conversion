from conversion.models import Cell, Column

LINE_MARGIN = 2

class CSVBuilder:
    def __init__(self, **kwargs):
        self._cells = {}
        self._columns = []

        self._current_col = 0
        self._current_row = 0

        ## 
        ##
        self.delimiter = kwargs.get("delimiter", ";")


        
    def build(self, cells: [Cell]):
        cells.sort(key=lambda cell: (cell.coordinates.y1, cell.coordinates.x1))

        previous_y1 = 0

        for cell in cells: 
            current_x1 = cell.coordinates.x1
            current_x2 = cell.coordinates.x2
            current_y1 = cell.coordinates.y1
            current_y2 = cell.coordinates.y2

            print(cell, ">>> " + cell.content)

            column = Column('', current_x1, current_x2, current_y1, current_y2)

            # checking for margin where should break line
            if (self.should_append_row(current_y1, previous_y1)):
                self.append_row()

            create_new_column = False

            if len(self._columns) > 0:
                # busca por colunas para adicionar a celula...
                _conflicted_columns = self.conflicted_columns(cell)

                # se celula pode pertencer a uma ou mais colunas...
                if len(_conflicted_columns) >= 1:
                    # seleciona a coluna mais proxima... (primeira)
                    conflicted_column = _conflicted_columns[0]

                    _id = "{0}::{1}".format(conflicted_column.name, self.current_row())

                    if self.cell_exists(_id):
                        if cell.content.strip() == '' and cell.content.strip() == self._cells[_id].content.strip():
                            continue
                        else:
                            create_new_column = True
                    else:
                        # update sizes ?? 
                        column = conflicted_column
                else:
                    create_new_column = True
            else:
                create_new_column = True

            if create_new_column:
                self.append_col()
                column.name = len(self._columns)
                # 
                self._columns.append(column)

            self._cells["%s::%d" % (column.name, self.current_row())] = cell

            previous_y1 = current_y1

    def conflicted_columns(self, cell):
        sort_x1 = cell.coordinates.x1 # --> Original: column.x1 

        # Lista todas as colunas em que a celula pode entrar e 
        # faz classificação onde x1 de celula e coluna for mais proximo
        _conflicted_columns: [Column] = list(filter(lambda c: c.cell_in_range(cell), self._columns))
        # _conflicted_columns.sort(key=lambda c: abs(c.x1 - cell.coordinates.x1))

        # sort by closest 
        _conflicted_columns.sort(key=lambda c: abs(c.y1 - cell.coordinates.y1))

        return _conflicted_columns

    def cell_exists(self, cell_name):
        return cell_name in self._cells
    
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ## 
    ## ROW FUNCIONS
    ## 
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def current_row(self):
        return self._current_row

    def append_row(self):
        self._current_row += 1

    def should_append_row(self, current_y1, previous_y1):
        return (current_y1 -LINE_MARGIN > previous_y1)# and (current_y1 > previous_y1)

    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ## 
    ## ROW FUNCIONS
    ## 
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def current_col(self):
        return self._current_col

    def append_col(self):
        self._current_col += 1

    def should_append_col(self, current_y1, previous_y2):
        return (current_y1 - LINE_MARGIN < previous_y2) and (current_y1 + LINE_MARGIN < previous_y2)

    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ## 
    ## WRITING FUNCIONS
    ## 
    ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def write(self, csv_file):
        self._columns.sort(key=lambda c: c.x1)

        CSV_FILE = csv_file
        CSV_ENCODING = "UTF-8"
        CSV_DELIMITER = self.delimiter

        with open(CSV_FILE, "a", encoding=CSV_ENCODING) as f:
            for row in range(self.current_row() + 1):
                for column in self._columns:
                    cell_name = '%s::%s' % (str(column.name), str(row))

                    f.write(('%s' + CSV_DELIMITER) % self._cells[cell_name].content
                        if cell_name in self._cells else CSV_DELIMITER)

                f.write('\r\n')

