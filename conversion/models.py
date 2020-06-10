
class Coordinate:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @classmethod
    def from_bbox(cls, bbox):
        return Coordinate(bbox[0], bbox[1], bbox[2], bbox[3])

    def __str__(self):
        return "left: %d, bottom: %d right: %d, top: %d" % (self.x1, self.x2, self.y1, self.y2)

class Column:
    def __init__(self, name, x1, x2, y1=None, y2=None):
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __str__(self):
        return """name:%s x1: %d, x2: %d""" % (self.name, self.x1, self.x2)

    def __repr__(self):
        return str(self)

    def width(self):
        return self.x2 - self.x1

    def cell_in_range(self, cell):
        return cell.coordinates.x1 < self.x2 \
               and cell.coordinates.x2 > self.x1

    def cell_position(self, cell):
        if self.cell_in_range(cell):
            return 0
        elif cell.coordinates.x2 < self.x1:
            return -1
        elif cell.coordinates.x1 > self.x2:
            return 1


class Cell:

    def __init__(self, name, content, coordinates):
        self.name = name
        self.content = content
        self.coordinates = Coordinate(coordinates.x1, coordinates.y1, coordinates.x2, coordinates.y2)

    def __str__(self):
        x1 = "{:.2f}".format(self.coordinates.x1).rjust(8)
        y1 = "{:.2f}".format(self.coordinates.y1).rjust(8)
        x2 = "{:.2f}".format(self.coordinates.x2).rjust(8)
        y2 = "{:.2f}".format(self.coordinates.y2).rjust(8)

        return """x1: {0}, y1: {1}, x2: {2}, y2: {3}""".format(x1, y1, x2, y2)

    def __repr__(self):
        return str(self)
