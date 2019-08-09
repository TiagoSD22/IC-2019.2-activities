from __future__ import annotations
from functools import reduce
from typing import List
import operator
import math


class StateMatrix:
    def __init__(self, rows: int, columns: int, elements: List[List]):
        self.rows = rows
        self.columns = columns
        self.elements = elements

    def __str__(self):
        msg: str = ""
        hyphens_qt: int = (9 * self.columns - 1)
        msg += "\n+{}+\n".format(hyphens_qt * "-")
        for i in range(self.rows):
            for j in range(self.columns):
                msg += "|  {x:^4}  ".format(x=str(self.elements[i][j])
                                            if self.elements[i][j] != self.rows * self.columns
                                            else " ")  # o bloco vazio é o de maior valor na sequência do puzzle
            msg += "|\n"
            if i != self.rows - 1:
                msg += "|{}|\n".format(hyphens_qt * "-")
        msg += "+{}+\n".format(hyphens_qt * "-")
        return msg

    def is_solved(self) -> bool:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.elements[i][j] != self.rows*i + j + 1:
                    return False
        return True

    def get_element_position(self, element: int) -> tuple:
        cords: List[tuple] = [(ind, self.elements[ind].index(element)) for ind in range(len(self.elements))
                              if element in self.elements[ind]]
        return cords[0]

    def get_blank_space_position(self) -> tuple:
        # o bloco vazio é o valor mais alto na sequência de números do puzzle que varia de acordo com o tamanho deste
        blank_value: int = self.rows * self.columns
        cords: tuple = self.get_element_position(blank_value)
        return cords

    def calculate_manhattan_distance(self, element: int) -> int:
        if element not in [item for sublist in self.elements for item in sublist]:
            return math.inf  # se o elemento não existe na matriz sua distância é infinita

        row_expected: int = (element - 1) // self.columns
        column_expected: int = (element - 1) % self.rows

        element_position: tuple = self.get_element_position(element)

        row_distance: int = abs(row_expected - element_position[0])
        column_distance: int = abs(column_expected - element_position[1])

        manhattan_distance: int = row_distance + column_distance
        return manhattan_distance


class TreeNode:
    def __init__(self, matrix: StateMatrix, tree_layer: int, children: List[TreeNode] = None, parent: TreeNode = None):
        self.matrix = matrix
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.tree_layer = tree_layer

    # heurística para estimar quão distante da solução o nó está, quanto menor o valor, melhor
    def get_distance_from_solution(self) -> int:
        distance: int = self.tree_layer

        distance += reduce(operator.add, map(self.matrix.calculate_manhattan_distance,
                                             [item for sublist in self.matrix.elements for item in sublist]))

        return distance

    def generate_possible_states(self):
        permutations: List[dict] = []
        up: dict = {"row": -1, "column": 0}
        left: dict = {"row": 0, "column": -1}
        down: dict = {"row": 1, "column": 0}
        right: dict = {"row": 0, "column": 1}
        permutations.extend([up, down, left, right])

        for permutation in permutations:
            try:
                child_state: StateMatrix = StateMatrix(self.matrix.rows, self.matrix.columns, self.matrix.elements)
                blank_position: tuple = self.matrix.get_blank_space_position()

                blank_row: int = blank_position[0]
                blank_column: int = blank_position[1]
                blank_value: int = self.matrix.rows * self.matrix.columns

                swap_row: int = permutation["row"] + blank_row
                swap_column: int = permutation["column"] + blank_column
                swap_value: int = child_state.elements[swap_row][swap_column]

                child_state.elements[swap_row][swap_column] = blank_value
                child_state.elements[blank_row][blank_column] = swap_value

                node_child: TreeNode = TreeNode(child_state, self.tree_layer + 1, parent=self)
                self.children.append(node_child)
            except IndexError:
                pass


def main():
    print("Executando main")
    #elements = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]
    #elements = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    elements = [[1,9,3], [4,5,6], [7,8,2]]
    m: StateMatrix = StateMatrix(3, 3, elements)
    node: TreeNode = TreeNode(m, 0)
    node.generate_possible_states()
    print("Estado original: ", node.matrix)
    for child in node.children:
        print("\nEstado possivel: ", child.matrix)


if __name__ == '__main__':
    main()
