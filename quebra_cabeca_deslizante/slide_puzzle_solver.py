#!/usr/bin/env python
"""Implementa um solucionador para um slide puzzle NxN

Este código implementa classes e modelos para solucionar instâncias de um problema slide puzzle de ordem NxN.
A estratégia para resolução é a de busca em largura em árvore de decisões utilizando heurísticas tipo A*. Por padrão,
o problema a ser resolvido será uma matriz de 3 linhas e 3 colunas (3x3), mas o programa é capaz de resolver instâncias
maiores, para isso, execute-o passando como argumento o valor a ser usado como ordem da matriz.
"""

from __future__ import annotations
from functools import reduce
from typing import List, Set
from decimal import Decimal
import operator
import random
import heapq
import copy
import sys

__author__ = "Tiago Siqueira Dionizio"
__email__ = "tiagosdionizio@gmail.com"


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
                if self.elements[i][j] != self.rows * i + j + 1:
                    return False
        return True

    # retorna uma tupla (linha, coluna) que informa a posição do elemento buscado na matriz
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
            return Decimal('Infinity')  # se o elemento não existe na matriz sua distância é infinita

        row_expected: int = (element - 1) // self.columns
        column_expected: int = (element - 1) % self.rows

        element_position: tuple = self.get_element_position(element)

        row_distance: int = abs(row_expected - element_position[0])
        column_distance: int = abs(column_expected - element_position[1])

        manhattan_distance: int = row_distance + column_distance
        return manhattan_distance

    def get_inversions_number(self) -> int:
        inversions: int = 0
        elements_list: List = [item for sublist in self.elements for item in sublist]
        blank_value: int = self.rows * self.columns
        for i in range((self.rows * self.columns) - 1):
            for j in range(i + 1, (self.rows * self.columns)):
                # se o valor da célula não for vazio e ela for maior do que uma célula subsequente não vazia,
                # então temos uma inversão
                if elements_list[i] != blank_value and elements_list[j] != blank_value \
                        and elements_list[i] > elements_list[j]:
                    inversions += 1
        return inversions

    def is_solvable(self) -> (bool, str):
        """
        Para um problema NxN ser solucionável, as seguintes condições devem ser respeitadas:
        1. Se N é impar, o número de inversões no estado inicial deve ser par
        2. Se N é par, o problema será solucionável se:
            2.1. A célula vazia está em uma linha de índice par, contando de baixo para cima e o número
                 de inversões é ímpar.
            2.2. A célula vazia está em uma linha de índice ímpar, contando de baixo para cima e o número
                 de inversões é par.
        Se estas condições não forem atendidas, o problema NÃO apresentará solução!
        """
        n: int = self.rows
        inversions: int = self.get_inversions_number()
        msg: str = ""
        if n % 2 == 1:  # n é ímpar
            solvable: bool = inversions % 2 == 0
            if not solvable:
                msg = "Problema de ordem ímpar({}), mas com quantidade ímpar de inversões({} inversões).\n\n" \
                    .format(n, inversions)
        else:  # n é par
            blank_position_row: int = self.rows - self.get_blank_space_position()[0]
            if blank_position_row % 2 == 0:  # a célula vazia está em uma linha par(de baixo para cima)
                solvable: bool = inversions % 2 == 1
                if not solvable:
                    msg = "Problema de ordem par({}), célula vazia em linha par, de baixo para cima, ({}), mas " \
                          "com quantidade par de inversões({}).\n".format(n, blank_position_row, inversions)
            else:  # a célula vazia está em uma linha ímpar(de baixo para cima)
                solvable: bool = inversions % 2 == 0
                if not solvable:
                    msg = "Problema de ordem par({}), célula vazia em linha ímpar, de baixo para cima, ({}), " \
                          "mas com quantidade ímpar de inversões({}).\n".format(n, blank_position_row, inversions)
        return solvable, msg


class TreeNode:
    def __init__(self, matrix: StateMatrix, tree_layer: int, children: List[TreeNode] = None, parent: TreeNode = None,
                 ditance_from_solution: int = -1):
        self.matrix = matrix
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.tree_layer = tree_layer
        if ditance_from_solution == -1:
            self.distance_from_solution = self.get_distance_from_solution()
        else:
            self.distance_from_solution = ditance_from_solution

    # heurística para estimar quão distante da solução o nó está, quanto menor o valor, melhor
    def get_distance_from_solution(self) -> int:
        blank_value: int = self.matrix.rows * self.matrix.columns

        distance: int = self.tree_layer
        distance += reduce(operator.add, map(self.matrix.calculate_manhattan_distance,
                                             [item for sublist in self.matrix.elements for item in sublist
                                              if item != blank_value]))

        return distance

    def generate_possible_states(self):
        permutations: List[dict] = []
        up: dict = {"row": -1, "column": 0}
        left: dict = {"row": 0, "column": -1}
        down: dict = {"row": 1, "column": 0}
        right: dict = {"row": 0, "column": 1}
        permutations.extend([up, down, left, right])

        for permutation in permutations:
            blank_position: tuple = self.matrix.get_blank_space_position()

            blank_row: int = blank_position[0]
            blank_column: int = blank_position[1]

            swap_row: int = permutation["row"] + blank_row
            swap_column: int = permutation["column"] + blank_column
            # o estado possível só será criado se a célula a ser trocada estiver dentro dos limites da matriz
            if 0 <= swap_row < self.matrix.rows and 0 <= swap_column < self.matrix.columns:
                # como a cópia de lista no python é, por padrão, shallow, precisamos fazer uma deep copy, pois
                # vamos alterar a matriz de estados, mas queremos manter a matriz original inalterada
                copy_matrix: List[List] = copy.deepcopy(self.matrix.elements)
                child_state: StateMatrix = StateMatrix(self.matrix.rows, self.matrix.columns, copy_matrix)

                blank_value: int = self.matrix.rows * self.matrix.columns
                swap_value: int = child_state.elements[swap_row][swap_column]

                child_state.elements[swap_row][swap_column] = blank_value
                child_state.elements[blank_row][blank_column] = swap_value

                child_distance = self.distance_from_solution - self.matrix.calculate_manhattan_distance(swap_value)
                child_distance += child_state.calculate_manhattan_distance(swap_value) + 1

                node_child: TreeNode = TreeNode(child_state, self.tree_layer + 1, parent=self,
                                                ditance_from_solution=child_distance)
                if self.parent is not None:
                    if node_child.matrix.elements != self.parent.matrix.elements:
                        self.children.append(node_child)
                else:
                    self.children.append(node_child)

    def __lt__(self, other: TreeNode):  # método usado para comparação no heap
        return self.distance_from_solution < other.distance_from_solution


class StateTree:
    def __init__(self, root: TreeNode):
        self.root = root

    # método para encontrar o caminho de um nó até a raíz da árvore
    def find_path_to_root(self, node: TreeNode) -> List[TreeNode]:
        path: List[TreeNode] = []
        current_node: TreeNode = node
        while current_node != self.root:
            path.append(current_node)
            current_node = current_node.parent
        path.append(current_node)
        path.reverse()  # a lista está de trás para frente, então precisamos usar o reverse
        return path


class SlidePuzzleSolver:
    def __init__(self, decision_tree: StateTree):
        self.decision_tree: StateTree = decision_tree
        self.puzzle_rows: int = decision_tree.root.matrix.rows
        self.puzzle_columns: int = decision_tree.root.matrix.columns

    def solve(self):
        self.show_header_message()
        nodes_added: Set[TreeNode] = set()
        execution_queue: List[TreeNode] = [self.decision_tree.root]
        solution_found: bool = False
        current_node: TreeNode = self.decision_tree.root
        final_node: TreeNode = self.decision_tree.root
        heapq.heapify(execution_queue)
        if current_node.matrix.is_solved():
            solution_found = True
            final_node = current_node

        while not solution_found:
            current_node = heapq.heappop(execution_queue)
            print("\nEstado escolhido:\n{}\nDistancia: {}".format(current_node.matrix,
                                                                  current_node.distance_from_solution))
            nodes_added.add(current_node)
            current_node.generate_possible_states()
            for child in current_node.children:
                if child.matrix.is_solved():
                    solution_found = True
                    final_node = child
                else:
                    if child.matrix.elements not in [node.matrix.elements for node in nodes_added]:
                        heapq.heappush(execution_queue, child)

        solution_path: List[TreeNode] = self.decision_tree.find_path_to_root(final_node)
        self.show_solution_steps(solution_path)

    def show_header_message(self):
        print("\n\nResolvendo instância do problema quebra cabeça deslizante.\nNúmero de linhas: {}"
              "\nNúmero de colunas: {}\n\nEstado inicial: {}\n\n".format(self.puzzle_rows, self.puzzle_columns,
                                                                         self.decision_tree.root.matrix))

    @staticmethod
    def show_solution_steps(solution_path: List[TreeNode]):
        print("Solução encontrada\n\n")
        for index in range(len(solution_path) - 1):
            if index == 0:
                print("\nEstado atual(Inicial)")
            else:
                print("\nEstado atual:")
            print(solution_path[index].matrix)
            blank_position_actual_step = solution_path[index].matrix.get_blank_space_position()
            blank_position_next_step = solution_path[index + 1].matrix.get_blank_space_position()
            if blank_position_actual_step[0] != blank_position_next_step[0]:  # moviento na vertical
                if blank_position_actual_step[0] - blank_position_next_step[0] > 0:  # branco foi para cima
                    step: str = "->Mova o bloco vazio para CIMA."
                else:  # branco foi para baixo
                    step: str = "->Mova o bloco vazio para BAIXO."
            else:  # movimento na horizontal
                if blank_position_actual_step[1] - blank_position_next_step[1] > 0:  # branco foi para a esquerda
                    step: str = "->Mova o bloco vazio para a ESQUERDA."
                else:  # branco foi para a direita
                    step: str = "->Mova o bloco vazio para a DIREITA."
            print(step, "\n")

        print("\nEstado final(Problema resolvido):\n", solution_path[len(solution_path) - 1].matrix)
        print("\nForam executados {} passos para encontrar a solução.\n\n".format(len(solution_path) - 1))


def generate_random_matrix(order: int) -> StateMatrix:
    solvable_matrix: bool = False
    while not solvable_matrix:
        elements: List = [x + 1 for x in range(order ** 2)]
        random.shuffle(elements)
        matrix: List[List] = [elements[index:index + order] for index in range(0, len(elements), order)]
        state_matrix: StateMatrix = StateMatrix(order, order, matrix)
        solvable_matrix = state_matrix.is_solvable()[0]
        if solvable_matrix:
            return state_matrix


def main():
    matrix_oder: int = 3
    try:
        arg: int = int(sys.argv[1])
        if arg > 1:
            matrix_oder = arg
            print("\nUtilizando valor argumento {} como ordem da matriz do puzzle.".format(matrix_oder))
        else:
            print("\nUtilizando valor padrão {} como ordem da matriz do puzzle, pois o valor passado como "
                  "argumento ({}) é menor que o mínimo aceitável(2).".format(matrix_oder, int(sys.argv[1])))
    except (ValueError, IndexError):
        print("\nUtilizando valor padrão {} como ordem da matriz do puzzle.".format(matrix_oder))
        pass

    initial_matrix_state: StateMatrix = generate_random_matrix(matrix_oder)
    solvable, msg = initial_matrix_state.is_solvable()
    if solvable:
        root: TreeNode = TreeNode(initial_matrix_state, 0)
        tree: StateTree = StateTree(root)

        slide_puzzle_solver: SlidePuzzleSolver = SlidePuzzleSolver(tree)
        slide_puzzle_solver.solve()
    else:
        print("\nInstância gerada não tem solução!\n", initial_matrix_state, "\n{}".format(msg))


if __name__ == '__main__':
    main()
