import math
import random
from abc import abstractmethod

import numpy as np

from ga.problem import Problem
from ga.individual import Individual

class IntVectorIndividual(Individual):

    def __init__(self, problem: Problem, num_genes: int):
        super().__init__(problem, num_genes)
        self.genome = np.full(num_genes, 0, dtype=int)

    def initialize(self, products: int):
        n = self.num_genes+10

        for i in range(self.num_genes):
            if (i > products-1):
                self.genome[i] =n
                n+=1
            else:
                self.genome[i] = i
        random.shuffle(self.genome)

        # inicializa o genoma com produtos e separadores ordenados de forma aleatória


    def swap_genes(self, other, index: int):
        aux = self.genome[index]
        self.genome[index] = other.genome[index]
        other.genome[index] = aux

    @abstractmethod
    def compute_fitness(self) -> float:
        pass

    @abstractmethod
    def better_than(self, other: "IntVectorIndividual") -> bool:
        pass
