from typing import List
from numpy import array

mock_list = []

sub_board1 = array([[0, 9, 0], [0, 5, 6], [0, 0, 8]])
sub_board2 = array([[0, 5, 6], [0, 1, 3], [0, 0, 0]])
sub_board3 = array([[0, 0, 0], [9, 2, 0], [6, 0, 7]])
sub_board4 = array([[0, 0, 1], [0, 0, 2], [0, 6, 0]])
sub_board5 = array([[0, 0, 0], [0, 0, 0], [0, 3, 4]])
sub_board6 = array([[5, 8, 0], [0, 4, 0], [0, 0, 0]])
sub_board7 = array([[7, 0, 0], [0, 0, 0], [5, 0, 0]])
sub_board8 = array([[6, 0, 0], [0, 0, 0], [4, 0, 8]])
sub_board9 = array([[0, 0, 0], [8, 9, 1], [0, 0, 0]])
mock_medium1: List = [
        sub_board1,
        sub_board2,
        sub_board3,
        sub_board4,
        sub_board5,
        sub_board6,
        sub_board7,
        sub_board8,
        sub_board9,
    ]
mock_list.append(("medium 1", mock_medium1))

sub_board1 = array([[0, 0, 0], [0, 0, 2], [0, 0, 7]])
sub_board2 = array([[0, 0, 0], [7, 0, 9], [8, 0, 0]])
sub_board3 = array([[0, 5, 3], [0, 4, 0], [0, 0, 0]])
sub_board4 = array([[0, 3, 0], [0, 0, 0], [0, 8, 9]])
sub_board5 = array([[0, 0, 0], [9, 0, 1], [0, 0, 2]])
sub_board6 = array([[0, 0, 6], [0, 0, 0], [0, 0, 7]])
sub_board7 = array([[4, 0, 0], [1, 0, 0], [8, 0, 0]])
sub_board8 = array([[0, 0, 0], [0, 6, 0], [0, 4, 0]])
sub_board9 = array([[2, 0, 0], [9, 0, 0], [0, 0, 0]])

mock_hard1: List = [
    sub_board1,
    sub_board2,
    sub_board3,
    sub_board4,
    sub_board5,
    sub_board6,
    sub_board7,
    sub_board8,
    sub_board9,
]
mock_list.append(("hard 1", mock_hard1))
