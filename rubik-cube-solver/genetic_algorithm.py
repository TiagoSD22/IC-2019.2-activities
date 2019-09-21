import copy
import operator
import random
from typing import List, Dict
from cube import Cube
from gene import Gene
from gene_enum import GeneEnum as GENE
from individual import Individual
import pandas as pd
import numpy as np


class GeneticAlgorithm:

    def __init__(self, first_cube: Cube, population_size: int, elite_size: int, mutation_rate: float,
                 max_generations: int):
        self.first_cube = first_cube
        self.__create_gene_dicts()
        self.__population: List[Individual] = self.create_initial_population(population_size)
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    def create_individual(self) -> Individual:
        rotations: List[str] = ["rotate_right", "rotate_left", "rotate_top", "rotate_bottom", "rotate_front",
                                "rotate_back"]
        orientations: List[str] = ["clockwise", "counterclockwise"]

        cube_copy: Cube = copy.deepcopy(self.first_cube)
        chromosome: List[Gene] = []

        for i in range(20):
            rotation = random.choice(rotations)
            orientation = random.choice(orientations)

            gene: Gene = Gene(self.__rotations_dict[rotation], self.__orientations_dict[orientation])
            chromosome.append(gene)

            rotation_function = getattr(cube_copy, rotation + "_" + orientation)
            rotation_function()

        individual: Individual = Individual(cube_copy, chromosome)
        return individual

    def create_initial_population(self, population_size: int) -> List[Individual]:
        population: List[Individual] = []

        for i in range(population_size):
            population.append(self.create_individual())

        return population

    def rank_population(self) -> List[float]:
        fitness_results: Dict[int, float] = {}

        for i in range(len(self.__population)):
            fitness_results[i] = self.__population[i].calculate_fitness()

        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def selection(population_ranked, elite_size: int) -> List[int]:
        selection_results: List[int] = []

        df = pd.DataFrame(np.array(population_ranked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, elite_size):
            selection_results.append(population_ranked[i][0])

        for i in range(0, len(population_ranked) - elite_size):
            pick = 100 * random.random()
            for j in range(0, len(population_ranked)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(population_ranked[i][0])
                    break

        return selection_results

    def create_mating_pool(self, selection_result: List[int]) -> List[Individual]:
        mating_pool: List[Individual] = []

        for i in range(len(selection_result)):
            index: int = selection_result[i]
            mating_pool.append(self.__population[index])

        return mating_pool

    def breed(self, parent1: Individual, parent2: Individual) -> Individual:
        first_parent: Individual = random.choice([parent1, parent2])
        second_parent: Individual = parent1 if first_parent == parent2 else parent2

        crossover_point1: int = int(random.random() * len(first_parent.chromosome))
        crossover_point2: int = int(random.random() * len(first_parent.chromosome))
        start_gene: int = min(crossover_point1, crossover_point2)
        end_gene: int = max(crossover_point1, crossover_point2)

        child_chromosome: List[Gene] = copy.deepcopy(first_parent.chromosome)

        for i in range(len(first_parent.chromosome)):
            if start_gene <= i <= end_gene:
                child_chromosome[i] = first_parent.chromosome[i]
            else:
                child_chromosome[i] = second_parent.chromosome[i]

        child_cube: Cube = copy.deepcopy(self.first_cube)
        self.__apply_chromosome_movements(child_cube, child_chromosome)

        child: Individual = Individual(child_cube, child_chromosome)
        return child

    def breed_population(self, mating_pool: List[Individual], elite_size: int):
        children: List[Individual] = []
        length: int = len(mating_pool) - elite_size
        pool = random.sample(mating_pool, len(mating_pool))

        for i in range(0, elite_size):
            children.append(mating_pool[i])

        for i in range(0, length):
            child: Individual = self.breed(pool[i], pool[len(mating_pool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual: Individual, mutation_rate: float):

        face_symbol: List[str] = [GENE.RIGHT.value, GENE.LEFT.value, GENE.TOP.value, GENE.BOTTOM.value,
                                  GENE.FRONT.value, GENE.BACK.value]

        orientation_symbol: List[str] = [GENE.CLOCKWISE.value, GENE.COUNTERCLOCKWISE.value]

        mutated_chromosome: List[Gene] = []

        for gene in individual.chromosome:
            if random.random() < mutation_rate:
                mutated_face: str = random.choice(face_symbol)
                mutated_orientation: str = random.choice(orientation_symbol)
                if mutated_face == gene.face_to_rotate:
                    if mutated_orientation == gene.orientation:
                        mutated_face = random.choice([other_face for other_face in face_symbol
                                                      if other_face != mutated_face])
                mutated_gene: Gene = Gene(mutated_face, mutated_orientation)
                mutated_chromosome.append(mutated_gene)
            else:
                mutated_chromosome.append(gene)

        self.__apply_chromosome_movements(individual.cube, mutated_chromosome)
        return individual

    def mutate_population(self, current_population, mutation_rate):
        mutated_population = []

        for individual in current_population:
            mutated_individual = self.mutate(individual, mutation_rate)
            mutated_population.append(mutated_individual)
        return mutated_population

    def create_next_generation(self, elite_size, mutation_rate):
        ranked_population = self.rank_population()
        selection_results = self.selection(ranked_population, elite_size)
        mating_pool = self.create_mating_pool(selection_results)
        children = self.breed_population(mating_pool, elite_size)
        next_generation = self.mutate_population(children, mutation_rate)
        return next_generation

    def run_natural_selection(self):
        for i in range(self.max_generations):
            #print("Geracao atual: ", i)
            self.__population = self.create_next_generation(self.elite_size, self.mutation_rate)

        best_individual_index = self.rank_population()[0][0]
        best_individual = self.__population[best_individual_index]
        return best_individual

    def __apply_chromosome_movements(self, cube: Cube, chromosome: List[Gene]):

        for gene in chromosome:
            face_key = [face_key for face_key, face_value in self.__rotations_dict.items()
                        if face_value == gene.face_to_rotate]

            orientation_key = [orientation_key for orientation_key, orientation_value in
                               self.__orientations_dict.items() if orientation_value == gene.orientation]

            rotation: str = face_key[0]

            orientation: str = orientation_key[0]

            rotation_function = getattr(cube, rotation + '_' + orientation)
            rotation_function()

    def __create_gene_dicts(self):
        rotations: List[str] = ["rotate_right", "rotate_left", "rotate_top", "rotate_bottom", "rotate_front",
                                "rotate_back"]
        orientations: List[str] = ["clockwise", "counterclockwise"]

        self.__rotations_dict: Dict[str, str] = dict()
        self.__orientations_dict: Dict[str, str] = dict()

        face_symbol: List[str] = [GENE.RIGHT.value, GENE.LEFT.value, GENE.TOP.value, GENE.BOTTOM.value,
                                  GENE.FRONT.value, GENE.BACK.value]

        orientation_symbol: List[str] = [GENE.CLOCKWISE.value, GENE.COUNTERCLOCKWISE.value]

        for i in range(len(rotations)):
            self.__rotations_dict[rotations[i]] = face_symbol[i]

        for i in range(len(orientations)):
            self.__orientations_dict[orientations[i]] = orientation_symbol[i]
