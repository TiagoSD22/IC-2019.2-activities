import numpy as np
from numpy import matrix


class Face:
    def __init__(self, color: int, rows: int = 3, columns: int = 3, elements: matrix = None):
        self.color = color
        self.rows = rows
        self.columns = columns
        self.elements = elements

    def is_solved(self) -> bool:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.elements[i][j] != self.color:
                    return False
        return True

    def rotate_clockwise(self):
        self.elements = np.rot90(self.elements, k=-1)

    def rotate_counterclockwise(self):
        self.elements = np.rot90(self.elements)

    def __str__(self) -> str:
        msg: str = ""
        hyphens_qt: int = (9 * self.columns - 1)
        msg += "\n+{}+\n".format(hyphens_qt * "-")
        for i in range(self.rows):
            for j in range(self.columns):
                msg += "|  {x:^4}  ".format(x=str(self.elements[i][j]))
            msg += "|\n"
            if i != self.rows - 1:
                msg += "|{}|\n".format(hyphens_qt * "-")
        msg += "+{}+\n".format(hyphens_qt * "-")
        return msg
