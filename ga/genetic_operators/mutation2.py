import numpy as np

from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation

class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = ind.num_genes
        posicaoInicial = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        valorATrocar = ind.genome[posicaoInicial]
        posicaoFinal = posicaoInicial
        while posicaoInicial == posicaoFinal:
            posicaoFinal = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        ind.genome = np.delete(ind.genome, posicaoInicial)
        ind.genome = np.insert(ind.genome, posicaoFinal, valorATrocar)

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
