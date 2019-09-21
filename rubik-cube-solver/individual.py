import math
from typing import List
from cube import Cube
from gene import Gene


class Individual:
    def __init__(self, cube: Cube, chromosome: List[Gene]):
        self.cube = cube
        self.chromosome = chromosome
        self.fitness: float = math.inf

    def calculate_fitness(self):
        self.fitness = (48 - self.cube.estimate_distance_from_solution())/48
        return self.fitness

