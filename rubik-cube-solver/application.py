import numpy as np
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


if __name__ == "__main__":
    order: int = 3
    cube: Cube = generate_cube(order)

    cube.rotate_right_clockwise()  # shift + r
    cube.rotate_top_clockwise()  # shift + u
    cube.rotate_bottom_clockwise() # shift + d
    cube.rotate_top_clockwise()  # shift + u
    cube.rotate_left_clockwise()  # shift + l
    cube.rotate_top_counterclockwise()  # u
    cube.rotate_bottom_counterclockwise()  # d
    cube.rotate_right_counterclockwise()  # r
    cube.rotate_left_counterclockwise()  # l
    cube.rotate_bottom_clockwise()  # shift + d
    cube.rotate_top_clockwise()  # shift + u
    cube.rotate_right_clockwise()  # shift + r
    cube.rotate_left_counterclockwise()  # l
    cube.rotate_top_counterclockwise()  # u
    cube.rotate_bottom_counterclockwise()  # d
    cube.rotate_right_clockwise()  # shift + r
    cube.rotate_top_clockwise()  # shift + u
    cube.rotate_bottom_counterclockwise()  # d
    cube.rotate_left_counterclockwise()  # l
    cube.rotate_front_clockwise()  # shift + f
    cube.rotate_top_counterclockwise()  # u

    faces_array: List[List] = adapt_cube_for_interactive(cube)
    cube_inter: CubeInteractive = CubeInteractive(N=order, faces_array=faces_array)
    cube_inter.draw_interactive()
    plt.show()
