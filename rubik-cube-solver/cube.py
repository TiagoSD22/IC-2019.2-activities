import copy
from face import Face
from numpy import flip
from numpy import array
from typing import Dict, List
from colorsEnum import ColorsEnum


class Cube:
    def __init__(self, order: int, faces: Dict[str, Face]):
        self.order: int = order
        self.top: Face = faces["TOP"]
        self.bottom: Face = faces["BOTTOM"]
        self.right: Face = faces["RIGHT"]
        self.left: Face = faces["LEFT"]
        self.front: Face = faces["FRONT"]
        self.back: Face = faces["BACK"]

    def is_solved(self) -> bool:
        for face in [self.back, self.front, self.bottom, self.top, self.right, self.left]:
            if not face.is_solved():
                return False
        return True

    def rotate_right_clockwise(self):
        self.right.rotate_clockwise()
        self.__rotate_right_clockwise_or_left_counterclockwise("RIGHT")

    def rotate_right_counterclockwise(self):
        self.right.rotate_counterclockwise()
        self.__rotate_left_clockwise_or_right_counterclockwise("RIGHT")

    def rotate_left_clockwise(self):
        self.left.rotate_clockwise()
        self.__rotate_left_clockwise_or_right_counterclockwise("LEFT")

    def rotate_left_counterclockwise(self):
        self.left.rotate_counterclockwise()
        self.__rotate_right_clockwise_or_left_counterclockwise("LEFT")

    def rotate_top_clockwise(self):
        self.top.rotate_clockwise()
        self.__rotate_top_clockwise_or_bottom_counterclockwise("TOP")

    def rotate_top_counterclockwise(self):
        self.top.rotate_counterclockwise()
        self.__rotate_bottom_clockwise_or_top_counterclockwise("TOP")

    def rotate_bottom_counterclockwise(self):
        self.bottom.rotate_counterclockwise()
        self.__rotate_top_clockwise_or_bottom_counterclockwise("BOTTOM")

    def rotate_bottom_clockwise(self):
        self.bottom.rotate_clockwise()
        self.__rotate_bottom_clockwise_or_top_counterclockwise("BOTTOM")

    def rotate_front_clockwise(self):
        self.front.rotate_clockwise()
        self.__rotate_front_clockwise_or_back_counterclockwise("FRONT")

    def rotate_front_counterclockwise(self):
        self.front.rotate_counterclockwise()
        self.__rotate_back_clockwise_or_front_counterclockwise("FRONT")

    def rotate_back_clockwise(self):
        self.back.rotate_clockwise()
        self.__rotate_back_clockwise_or_front_counterclockwise("BACK")

    def rotate_back_counterclockwise(self):
        self.back.rotate_counterclockwise()
        self.__rotate_front_clockwise_or_back_counterclockwise("BACK")

    def __rotate_front_clockwise_or_back_counterclockwise(self, face: str):
        if face == "FRONT":
            change_index: int = self.order - 1
        else:
            change_index: int = 0

        aux1: array = copy.deepcopy(self.top.elements[change_index])
        # precisamos inverter a coluna ao reposicioná-la como linha no topo
        self.top.elements[change_index] = flip(copy.deepcopy(self.left.elements[:, change_index]))
        aux2: array = copy.deepcopy(self.right.elements[:, self.order - 1 - change_index])
        self.right.elements[:, self.order - 1 - change_index] = copy.deepcopy(aux1)
        aux1 = copy.deepcopy(self.bottom.elements[self.order - 1 - change_index])
        self.bottom.elements[self.order - 1 - change_index] = flip(copy.deepcopy(aux2))
        self.left.elements[:, change_index] = copy.deepcopy(aux1)

    def __rotate_back_clockwise_or_front_counterclockwise(self, face: str):
        if face == "FRONT":
            change_index: int = self.order - 1
        else:
            change_index: int = 0

        aux1: array = copy.deepcopy(self.top.elements[change_index])
        self.top.elements[change_index] = copy.deepcopy(self.right.elements[:, self.order - 1 - change_index])
        aux2: array = copy.deepcopy(self.left.elements[:, change_index])
        self.left.elements[:, change_index] = copy.deepcopy(flip(aux1))
        aux1 = copy.deepcopy(self.bottom.elements[self.order - 1 - change_index])
        self.bottom.elements[self.order - 1 - change_index] = copy.deepcopy(aux2)
        self.right.elements[:, self.order - 1 - change_index] = copy.deepcopy(flip(aux1))

    def __rotate_right_clockwise_or_left_counterclockwise(self, face: str):
        if face == "RIGHT":
            column_index: int = self.order - 1
        else:
            column_index: int = 0

        aux1: array = copy.deepcopy(self.top.elements[:, column_index])
        self.top.elements[:, column_index] = copy.deepcopy(self.front.elements[:, column_index])
        aux2: array = copy.deepcopy(self.back.elements[:, self.order - 1 - column_index])
        # movimentos do tipo BACK -> TOP, TOP -> BACK, BACK -> BOTTOM, BOTTOM -> BACK, devem ter a coluna rotacionada
        # primeiro, pois a ordem dos elementos é invertida nesse tipo de movimento
        self.back.elements[:, self.order - 1 - column_index] = copy.deepcopy(flip(aux1))
        aux1 = copy.deepcopy(self.bottom.elements[:, column_index])
        self.bottom.elements[:, column_index] = copy.deepcopy(flip(aux2))
        self.front.elements[:, column_index] = copy.deepcopy(aux1)

    def __rotate_left_clockwise_or_right_counterclockwise(self, face: str):
        if face == "RIGHT":
            column_index: int = self.order - 1
        else:
            column_index: int = 0

        aux1: array = copy.deepcopy(self.front.elements[:, column_index])
        self.front.elements[:, column_index] = copy.deepcopy(self.top.elements[:, column_index])
        aux2: array = copy.deepcopy(self.bottom.elements[:, column_index])
        self.bottom.elements[:, column_index] = copy.deepcopy(aux1)
        aux1 = copy.deepcopy(self.back.elements[:, self.order - 1 - column_index])
        # movimentos do tipo BACK -> TOP, TOP -> BACK, BACK -> BOTTOM, BOTTOM -> BACK, devem ter a coluna rotacionada
        # primeiro, pois a ordem dos elementos é invertida nesse tipo de movimento
        self.back.elements[:, self.order - 1 - column_index] = copy.deepcopy(flip(aux2))
        self.top.elements[:, column_index] = copy.deepcopy(flip(aux1))

    def __rotate_top_clockwise_or_bottom_counterclockwise(self, face: str):
        if face == "TOP":
            column_index: int = 0
        else:
            column_index: int = self.order - 1

        aux1: array = copy.deepcopy(self.left.elements[column_index])
        self.left.elements[column_index] = copy.deepcopy(self.front.elements[column_index])
        aux2: array = copy.deepcopy(self.back.elements[column_index])
        self.back.elements[column_index] = copy.deepcopy(aux1)
        aux1 = copy.deepcopy(self.right.elements[column_index])
        self.right.elements[column_index] = copy.deepcopy(aux2)
        self.front.elements[column_index] = copy.deepcopy(aux1)

    def __rotate_bottom_clockwise_or_top_counterclockwise(self, face: str):
        if face == "TOP":
            column_index: int = 0
        else:
            column_index: int = self.order - 1

        aux1: array = copy.deepcopy(self.front.elements[column_index])
        self.front.elements[column_index] = copy.deepcopy(self.left.elements[column_index])
        aux2: array = copy.deepcopy(self.right.elements[column_index])
        self.right.elements[column_index] = copy.deepcopy(aux1)
        aux1 = copy.deepcopy(self.back.elements[column_index])
        self.back.elements[column_index] = copy.deepcopy(aux2)
        self.left.elements[column_index] = copy.deepcopy(aux1)

    def __str__(self):
        res: str = ""
        layers: List[str] = ["TOP", "BOTTOM", "RIGHT", "LEFT", "FRONT", "BACK"]
        index: int = 0
        for face in [self.top, self.bottom, self.right, self.left, self.front, self.back]:
            res += "\nFace({}) de cor: {}\n".format(layers[index], ColorsEnum(face.color).name)
            res += str(face)
            index += 1
        res += "\nCubo montado: {}".format(self.is_solved())
        return res
