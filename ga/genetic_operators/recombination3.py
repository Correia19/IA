import numpy as np

from ga.genetic_algorithm import GeneticAlgorithm
from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual

class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        child1 = [None] * num_genes
        child2 = [None] * num_genes

        for i in range(0, num_genes, 2):
            child1[i] = ind1.genome[i]
        while None in child1:
            for k in range(0, num_genes):
                if child1[k] == None:
                    for l in range(0, num_genes):
                        if ind2.genome[l] not in child1:
                            child1[k] = ind2.genome[l]
                            break

        for i in range(0, num_genes, 2):
            child2[i] = ind2.genome[i]
        while None in child2:
            for k in range(0, num_genes):
                if child2[k] == None:
                    for l in range(0, num_genes):
                        if ind1.genome[l] not in child2:
                            child2[k] = ind1.genome[l]
                            break

        ind1.genome = child1
        ind2.genome = child2

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"