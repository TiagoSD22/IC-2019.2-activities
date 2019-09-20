from __future__ import annotations
import copy
from functools import reduce
import operator
from cube import Cube
from typing import List
from typing import Dict
from face import Face


class TreeNode:
    def __init__(self, cube: Cube, tree_layer: int, children: List[TreeNode] = None, parent: TreeNode = None,
                 distance_from_solution: int = -1):
        self.cube = cube
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.tree_layer = tree_layer
        if distance_from_solution == -1:
            self.distance_from_solution = self.get_distance_from_solution_and_origin()
        else:
            self.distance_from_solution = distance_from_solution

    # heurística para estimar quão distante da solução o nó está, quanto menor o valor, melhor
    def get_distance_from_solution_and_origin(self) -> int:
        distance: int = self.tree_layer

        faces: List[Face] = [self.cube.front, self.cube.back, self.cube.top, self.cube.bottom,
                             self.cube.left, self.cube.right]
        distance += reduce(operator.add, [face.get_total_wrong_pieces() for face in faces])

        return distance

    def generate_possible_states(self):
        rotations: List[str] = ["rotate_right", "rotate_left", "rotate_top", "rotate_bottom", "rotate_front",
                                "rotate_back"]
        orientations: List[str] = ["clockwise", "counterclockwise"]

        for rotation in rotations:
            for orientation in orientations:
                # como a cópia de lista no python é, por padrão, shallow, precisamos fazer uma deep copy, pois
                # vamos alterar a matriz de estados, mas queremos manter a matriz original inalterada
                copy_faces: Dict[str, Face] = copy.deepcopy(self.cube.get_faces())
                child_state: Cube = Cube(self.cube.order, copy_faces)

                rotation_function = getattr(child_state, rotation + "_" + orientation)
                rotation_function()

                child_distance: int = self.distance_from_solution + child_state.estimate_distance_from_solution()

                node_child: TreeNode = TreeNode(child_state, self.tree_layer + 1, parent=self,
                                                distance_from_solution=child_distance)
                if self.parent is not None:
                    if self.cube.get_faces() != child_state.get_faces():
                        self.children.append(node_child)
                else:
                    self.children.append(node_child)

    def __lt__(self, other: TreeNode):  # método usado para comparação no heap
        return self.get_distance_from_solution_and_origin() < other.get_distance_from_solution_and_origin()