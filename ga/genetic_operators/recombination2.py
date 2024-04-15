from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination

class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        child1 = []
        child2 = []

        for i in range(0, cut1):
            child1.append(ind1.genome[i])
        for k in range(0, num_genes):
            if ind2.genome[k] not in child1:
                child1.append(ind2.genome[k])
        i,k = 0, 0

        for i in range(0, cut1):
            child2.append(ind2.genome[i])
        for k in range(0, num_genes):
            if ind1.genome[k] not in child2:
                child2.append(ind1.genome[k])

        ind1.genome = child1
        ind2.genome = child2

    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
