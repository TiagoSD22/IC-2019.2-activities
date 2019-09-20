import heapq
from typing import Set, List
from state_tree import StateTree
from tree_node import TreeNode


class RubikCubeSolver:
    def __init__(self, decision_tree: StateTree):
        self.decision_tree: StateTree = decision_tree

    def solve(self):
        nodes_added: Set[TreeNode] = set()
        execution_queue: List[TreeNode] = [self.decision_tree.root]
        solution_found: bool = False
        current_node: TreeNode = self.decision_tree.root
        final_node: TreeNode = self.decision_tree.root
        heapq.heapify(execution_queue)

        if current_node.cube.is_solved():
            solution_found = True
            final_node = current_node

        while not solution_found:
            current_node = heapq.heappop(execution_queue)

            print(current_node.cube, " Distancia: ", current_node.get_distance_from_solution_and_origin())

            nodes_added.add(current_node)
            current_node.generate_possible_states()
            for child in current_node.children:
                if child.cube.is_solved():
                    solution_found = True
                    final_node = child
                else:
                    if child.cube.get_faces() not in [node.cube.get_faces() for node in nodes_added]:
                        heapq.heappush(execution_queue, child)

        solution_path: List[TreeNode] = self.decision_tree.find_path_to_root(final_node)
        print("Solucao encontrada. {} movimentos executados.", len(solution_path))
        #self.show_solution_steps(solution_path)
