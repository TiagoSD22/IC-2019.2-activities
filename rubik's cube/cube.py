import copy
import numpy as np
from Face import Face
from numpy import array
from typing import Dict, List
from ColorsEnum import ColorsEnum


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
        self.__rotate_right_or_left_counter(self.order - 1)

    def rotate_right_counterclockwise(self):
        self.right.rotate_counterclockwise()
        self.__rotate_left_or_right_counter(self.order - 1)

    def rotate_left_clockwise(self):
        self.left.rotate_clockwise()
        self.__rotate_left_or_right_counter(0)

    def rotate_left_counterclockwise(self):
        self.left.rotate_counterclockwise()
        self.__rotate_right_or_left_counter(0)

    def __rotate_right_or_left_counter(self, changing_index: int):
        aux1: array = copy.deepcopy(self.top.elements[:, changing_index])
        self.top.elements[:, changing_index] = self.front.elements[:, changing_index]
        aux2: array = copy.deepcopy(self.back.elements[:, changing_index])
        self.back.elements[:, changing_index] = aux1
        aux1 = copy.deepcopy(self.bottom.elements[:, changing_index])
        self.bottom.elements[:, changing_index] = aux2
        self.front.elements[:, changing_index] = aux1

    def __rotate_left_or_right_counter(self, changing_index: int):
        aux1: array = copy.deepcopy(self.front.elements[:, changing_index])
        self.front.elements[:, changing_index] = self.top.elements[:, changing_index]
        aux2: array = copy.deepcopy(self.bottom.elements[:, changing_index])
        self.bottom.elements[:, changing_index] = aux1
        aux1 = copy.deepcopy(self.back.elements[:, changing_index])
        self.back.elements[:, changing_index] = aux2
        self.top.elements[:, changing_index] = aux1

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
