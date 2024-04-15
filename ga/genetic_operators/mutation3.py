from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        cut2 = cut1
        while (cut1 == cut2):
            cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        subarray = ind.genome[cut1:cut2]
        inverted_subarray = subarray[::-1]

        ind.genome[cut1:cut2] = inverted_subarray

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
