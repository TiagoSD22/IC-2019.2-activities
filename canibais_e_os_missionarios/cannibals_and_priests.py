#!/usr/bin/env python
"""Implementa um solucionador para o problema dos canibais e missionários

Este código implementa classes e modelos para solucionar instâncias de um problema dos missionários e canibais.
O problema consiste em atravessar um grupo formado, por padrão, por 3 canibais e 3 missionários, de um lado do rio para
o outro lado. Para isso, existe uma canoa capaz de transportar duas pessoas por vez. Contudo, existe uma restrição para
o problema, o número de canibais de um lado do rio não pode ser maior do que o de missionários no mesmo lado, pois se
isso acontecer, os canibais comerão os missionários. Para alterar parâmetros como a quantidade de missionários ou de
canibais que devem ser salvos, execute o script passando como argumento o referido valor, ou -1 para tornar opcional
salvar alguém daquele grupo.
"""

from __future__ import annotations
from typing import List
from enum import Enum
import random
import sys

__author__ = "Tiago Siqueira Dionizio"
__email__ = "tiagosdionizio@gmail.com"


class Side(Enum):
    LEFT = "esquerda"
    RIGHT = "direita"


class ProblemParams:  # classe para configurar parâmetros de uma instância do problema dos canibais e missionários
    def __init__(self, cannibals_total_qt: int = 3, priests_total_qt: int = 3, boat_initial_side: Side = Side.LEFT,
                 cannibals_to_save: int = 3, priests_to_save: int = 3):
        self.cannibals_total_qt: int = cannibals_total_qt
        self.priests_total_qt: int = priests_total_qt
        self.boat_initial_side: Side = boat_initial_side
        self.cannibals_to_save: int = cannibals_to_save
        self.priests_to_save: int = priests_to_save


class State:
    def __init__(self, cannibals_on_left: int, priests_on_left: int,
                 cannibals_on_right: int, priests_on_right: int, boat_side: Side):
        self.cannibals_on_left: int = cannibals_on_left
        self.cannibals_on_right: int = cannibals_on_right
        self.priests_on_left: int = priests_on_left
        self.priests_on_right: int = priests_on_right
        self.boat_side: Side = boat_side

    def __str__(self):  # método para printar as informações de um estado com o método print
        msg: str = "\nMARGEM ESQUERDA:\t\t MARGEM DIREITA:\n"
        msg += "Canibais: {}\t\t\t Canibais: {}\n".format(self.cannibals_on_left, self.cannibals_on_right)
        msg += "Missionários: {}\t\t\t Missionários: {}\n".format(self.priests_on_left, self.priests_on_right)
        msg += "Margem da canoa: {}\n".format(str(self.boat_side.value).upper())
        return msg

    def is_valid(self) -> bool:
        # quantidade de missionários e canibais em ambas as margens deve ser maior ou igual a zero
        condition1: bool = self.priests_on_left >= 0 and self.cannibals_on_left >= 0
        condition2: bool = self.priests_on_right >= 0 and self.cannibals_on_right >= 0
        # quantidade de canibais em ambas as margens não deve ser maior do que a de missionários na mesma margem
        condition3: bool = self.priests_on_left == 0 or self.cannibals_on_left <= self.priests_on_left
        condition4: bool = self.priests_on_right == 0 or self.cannibals_on_right <= self.priests_on_right
        # estado é válido se todas as condições forem satisfeitas
        return condition1 and condition2 and condition3 and condition4


class TreeNode:
    def __init__(self, state: State, children: List[TreeNode] = None, parent: TreeNode = None):
        self.state = state
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent

    def generate_children(self):
        possible_movements: List[dict] = []
        movement1: dict = {"cannibal": 2, "priest": 0}  # move 2 canibais e 0 missionários
        movement2: dict = {"cannibal": 1, "priest": 1}  # move 1 canibal e 1 missionário
        movement3: dict = {"cannibal": 0, "priest": 2}  # move 0 canibais e 2 missionários
        movement4: dict = {"cannibal": 1, "priest": 0}  # move 1 canibal e 0 missionários
        movement5: dict = {"cannibal": 0, "priest": 1}  # move 0 canibais e 1 missionário
        possible_movements.extend([movement1, movement2, movement3, movement4, movement5])
        # permite gerar árvore de decisões de forma aleatória para encontrar diferentes soluções de uma mesma instância
        random.shuffle(possible_movements)

        for movement in possible_movements:  # gerando os nós de possíveis decisões
            child_state: State = State(self.state.cannibals_on_left, self.state.priests_on_left,
                                       self.state.cannibals_on_right, self.state.priests_on_right,
                                       self.state.boat_side)

            if self.state.boat_side == Side.LEFT:  # movendo da margem esquerda para a direita
                child_state.cannibals_on_left -= movement["cannibal"]
                child_state.priests_on_left -= movement["priest"]
                child_state.cannibals_on_right += movement["cannibal"]
                child_state.priests_on_right += movement["priest"]
                child_state.boat_side = Side.RIGHT
            else:  # movendo da margem direita para a esquerda
                child_state.cannibals_on_right -= movement["cannibal"]
                child_state.priests_on_right -= movement["priest"]
                child_state.cannibals_on_left += movement["cannibal"]
                child_state.priests_on_left += movement["priest"]
                child_state.boat_side = Side.LEFT

            if child_state.is_valid():
                child_node: TreeNode = TreeNode(child_state, parent=self)
                self.children.append(child_node)


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


class CannibalsAndPriestsProblem:
    def __init__(self, problem_params: ProblemParams, decision_tree: StateTree):
        self.problem_params = problem_params
        self.decision_tree = decision_tree

    def solve(self):
        self.show_header_message()
        path: List[TreeNode] = [self.decision_tree.root]
        solution_found: bool = False
        current_node_index: int = 0
        current_node: TreeNode = path[current_node_index]
        while not solution_found and current_node_index < len(path):
            if self.is_final_state(current_node):  # nó solução encontrado
                solution_found = True
                current_node_index -= 1
            else:  # percorre a árvore de decisões com uma estratégia de busca em largura
                if len(current_node.children) == 0:
                    current_node.generate_children()
                    path.extend(current_node.children)
            current_node_index += 1
            current_node = path[current_node_index]

        if solution_found:
            solution_path: List[TreeNode] = self.decision_tree.find_path_to_root(current_node)
            print_solution(solution_path)

        else:  # dependendo da instância, o problema pode não ter solução
            print("\n\nInstância sem solução!\n\n")

    def is_final_state(self, node: TreeNode):
        if self.problem_params.boat_initial_side == Side.LEFT:
            condition1: bool = node.state.cannibals_on_right == self.problem_params.cannibals_to_save
            condition2: bool = node.state.priests_on_right == self.problem_params.priests_to_save
        else:
            condition1: bool = node.state.cannibals_on_left == self.problem_params.cannibals_to_save
            condition2: bool = node.state.priests_on_left == self.problem_params.priests_to_save

        return (condition1 or self.problem_params.cannibals_to_save == -1) and \
               (condition2 or self.problem_params.priests_to_save == -1)

    def show_header_message(self):
        cannibals_to_save_msg: str = str(self.problem_params.cannibals_to_save)
        if cannibals_to_save_msg == "-1":
            cannibals_to_save_msg = "qualquer quantidade de"
        priests_to_save_msg: str = str(self.problem_params.priests_to_save)
        if priests_to_save_msg == "-1":
            priests_to_save_msg = "qualquer quantidade de"
        print("\n\nResolvendo instância do problema dos canibais e missionários."
              "\n\nTotal de canibais: {}.\nTotal de missionários: {}.\nMargem de origem: {}.\n"
              "\n\nCondição de sucesso:\nAtravessar: {} canibais.\nAtravessar: {} missionários.\n\n"
              .format(self.problem_params.cannibals_total_qt, self.problem_params.priests_total_qt,
                      str(self.problem_params.boat_initial_side.value).upper(), cannibals_to_save_msg,
                      priests_to_save_msg))


# método para descrever os passos realizados para obter a solução da instância do problema
def print_solution(solution_path: List[TreeNode]):
    print("\nSolução encontrada\n")
    print("Estado inicial\n", solution_path[0].state)
    for index in range(1, len(solution_path)):
        step: str = ""

        cannibals_moved: int = abs(solution_path[index-1].state.cannibals_on_left -
                                   solution_path[index].state.cannibals_on_left)
        priests_moved: int = abs(solution_path[index-1].state.priests_on_left -
                                 solution_path[index].state.priests_on_left)
        if cannibals_moved > 0:
            if cannibals_moved > 1:
                step += "->Mova {} canibais".format(cannibals_moved)
            else:
                step += "->Mova {} canibal".format(cannibals_moved)

        if priests_moved > 0:
            if len(step) > 0:
                step += " e"
            else:
                step += "->Mova"
            if priests_moved > 1:
                step += " {} missionários".format(priests_moved)
            else:
                step += " {} missionário".format(priests_moved)

        direction: str = " da {} para a {}".format(str(solution_path[index - 1].state.boat_side.value).upper(),
                                                   str(solution_path[index].state.boat_side.value).upper())

        step += "{}.\n".format(direction)
        print(step)
        if index == len(solution_path) - 1:
            print("Estado final(Problema resolvido)\n", solution_path[index].state)
        else:
            print("Estado atual\n", solution_path[index].state)

    print("\nForam executados {} passos para encontrar a solução.\n\n".format(len(solution_path) - 1))


def generate_problem_params(total_cannibals: int, total_priests: int, 
                            cannibals_to_save: int, priests_to_save: int, 
                            boat_initial_side: Side) -> ProblemParams:

    """ Configuração dos parâmetros do problema
    :param total_cannibals: total de canibais no problema
    :param total_priests: total de missionários no problema
    :param cannibals_to_save: quantidade de canibais que devem chegar à outra margem do rio (-1 para tornar opcional)
    :param priests_to_save: quantidade de missionários que devem chegar à outra margem do rio (-1 para tornar opcional)
    :param boat_initial_side: margem de origem dos missionários e canibais
    :return: um objeto do tipo ProblemParams com as configurações informadas
    """

    params: ProblemParams = ProblemParams(total_cannibals, total_priests, boat_initial_side,
                                          cannibals_to_save, priests_to_save)

    return params


def main():
    total_cannibals: int = 3
    total_priests: int = 3
    cannibals_to_save: int = 3
    priests_to_save: int = 3
    boat_initial_side: Side = Side.LEFT

    try:  # caso o script seja chamado com argumentos
        total_cannibals = int(sys.argv[1])
        total_priests = int(sys.argv[2])
        cannibals_to_save = int(sys.argv[3])
        priests_to_save = int(sys.argv[4])
        initial_side: str = sys.argv[5]
        if initial_side in ["L", "l"]:
            boat_initial_side = Side.LEFT
        elif initial_side in ["R", "r"]:
            boat_initial_side = Side.RIGHT
    except IndexError:
        print("\n\nPrograma sendo executado com alguns argumentos default.")
        pass

    params = generate_problem_params(total_cannibals, total_priests, cannibals_to_save, priests_to_save,
                                     boat_initial_side)

    if params.boat_initial_side == Side.LEFT:  # margem de origem dos canibais e missionários é a ESQUERDA
        initial_state: State = State(params.cannibals_total_qt, params.priests_total_qt, 0, 0,
                                     params.boat_initial_side)
        root: TreeNode = TreeNode(initial_state)
    else:  # margem de origem dos canibais e missionários é a DIREITA
        initial_state: State = State(0, 0, params.cannibals_total_qt, params.priests_total_qt,
                                     params.boat_initial_side)
        root: TreeNode = TreeNode(initial_state)

    tree: StateTree = StateTree(root)

    problem: CannibalsAndPriestsProblem = CannibalsAndPriestsProblem(params, tree)
    problem.solve()


if __name__ == '__main__':
    main()
