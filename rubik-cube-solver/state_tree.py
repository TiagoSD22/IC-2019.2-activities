from typing import List
from tree_node import TreeNode


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