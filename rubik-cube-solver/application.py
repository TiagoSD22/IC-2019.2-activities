import random
import numpy as np
from rubik_cube_solver import RubikCubeSolver
from state_tree import StateTree
from tree_node import TreeNode
from cube import Cube
from face import Face
import matplotlib.pyplot as plt
from typing import Dict, List
from cube_interactive import Cube as CubeInteractive


def generate_cube(order: int = 3) -> Cube:
    faces: Dict[str, Face] = {}
    layers: List[str] = ["TOP", "BOTTOM", "LEFT", "RIGHT", "FRONT", "BACK"]
    for i in range(6):
        matrix: np.matrix = np.array(list([[i] * order] * order))
        face = Face(i, order, order, matrix)
        faces[layers[i]] = face
    cube_returned: Cube = Cube(order, faces)
    return cube_returned


def adapt_cube_for_interactive(cube: Cube) -> List[List]:
    faces_array: List[List] = []
    cube_faces: List = [cube.top.elements, cube.bottom.elements, cube.left.elements, cube.right.elements,
                        cube.back.elements, cube.front.elements]
    for face in cube_faces:
        temp: List = []
        for j in range(cube.order):
            temp.append([e for e in face[:, j][::-1]])
        face_list = [e for sublist in temp for e in sublist]
        faces_array.append(face_list)
    return faces_array


def scramble_cube(cube: Cube, minimum_movements: int = 50, maximum_movements: int = 100):
    rotations: List[str] = ["rotate_right", "rotate_left", "rotate_top", "rotate_bottom", "rotate_front",
                            "rotate_back"]
    orientations: List[str] = ["clockwise", "counterclockwise"]

    n_movements: int = random.randrange(minimum_movements, maximum_movements + 1, 1)

    for i in range(n_movements):
        rotation = random.choice(rotations)
        orientation = random.choice(orientations)

        rotation_function = getattr(cube, rotation + "_" + orientation)
        rotation_function()


if __name__ == "__main__":
    order: int = 3
    cube: Cube = generate_cube(order)

    scramble_cube(cube, 200, 1000)

    root: TreeNode = TreeNode(cube, 0)
    tree: StateTree = StateTree(root)

    solver: RubikCubeSolver = RubikCubeSolver(tree)

    #solver.solve()  # busca com heuristica nao esta funcionando

    cube_inter: CubeInteractive = CubeInteractive(N=order, faces_array=adapt_cube_for_interactive(cube))
    cube_inter.draw_interactive()
    plt.show()
