import random

from ga.individual_int_vector import IntVectorIndividual

class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.colisoes = 0
        self.custoPorForklift = []
        self.max_steps= 0

    def compute_fitness(self) -> float:
        self.obtain_all_path()
        self.fitness = self.colisoes + self.max_steps -1                                                           #esta analisa o menor custo com o maximo steps de um só forklift
        #self.fitness = self.colisoes + self.max_steps + sum(self.custoPorForklift)                             esta analisa o menor custo junto com o passos totais com colisoes
        #self.fitness = self.colisoes + sum(self.custoPorForklift)                                              esta analisa o menor custo dos passos totais com colisoes
        return self.fitness

    def obtain_all_path(self):
        custo = 0                                                                                               #guarda o indice do forklift que estamos a analisar
        custoPorForklift = []                                                                                   # guarda o custo de cada forklift
        forklift = 0                                                                                            #guarda o indice do forklift do array forklifts
        pathdoForklift = []                                                                                     #guarda o path de cada forklift enquanto é calculado
        Paths = []                                                                                              #guarda o path dos forklifts por index de forklift, ou seja (Paths[0] = path do forklift 0)
        posicaoAnterior = self.problem.forklifts[forklift]                                                      #variavel que guarda a primeira celula do pair
        for i in range(self.num_genes):                                                                         #precorre o genoma (num_genes = num_produtos+ num_forklifts-1), -1 porque o primeiro forklift nao é guardado no genoma
            if (self.genome[i] > self.num_genes):                                                               #verifica se o valor é maior do que o num_genes ou seja se é um novo forklift
                for k in reversed(range(len(self.problem.agent_search.pairs))):                                 #percorre os pairs ao contrario(uma vez que os pairs da saida estão no fim do array)
                                                                                                                # para encontrar o pair que liga a celula anterior à saida
                    if (((self.problem.agent_search.pairs[k].cell1 == posicaoAnterior) and (
                            self.problem.agent_search.pairs[k].cell2 == self.problem.agent_search.exit))):      #vamos ver qual é a posição no array pairs que corresponde à celula anterior e à saida
                                                                                                                #Nota que como a saida é sempre a segunda celula no array não temos de verificar se é a primeira ou a segunda
                        if (posicaoAnterior == self.problem.forklifts[forklift]):                               #Se estivermos a ir buscar o primeiro caminho( a começar num forklift) guardamos o primeiro paço do caminho
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[k].path
                        else:                                                                                   #caso contrário não guardamos para não ficarem passos repetidos
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[k].path[1:]

                        custo += self.problem.agent_search.pairs[k].value                                       # adicionamos o custo do pair ao custo anterior enquanto trabalharmos no mesmo forklift
                        custoPorForklift.append(custo)                                                          # adicionamos o custo final de um forklift ao array de custos
                        custo = 0                                                                               # resetamos o custo para o proximo forklift

                        forklift += 1                                                                           #incrementamos o indice do forklift
                        Paths.append(pathdoForklift)                                                            #guardamos o path do forklift no array Paths, ou seja, o indice do forklift corresponde ao indice do seu caminho no array paths
                        pathdoForklift = []                                                                     #limpamos a variável para que possa ser usada para o próximo forklift
                        posicaoAnterior = self.problem.forklifts[forklift]                                      #colocamos a posição anterior como a posição do novo forklift
                        break

            if (self.genome[i] < len(self.problem.products)):                                                   #verifica se o valor corresponde a um produto
                posicaoSeguinte = self.problem.products[self.genome[i]]                                         #guarda a posição do produto
                for j in range(len(self.problem.agent_search.pairs)):                                           #percorre o array pairs
                    if ((self.problem.agent_search.pairs[j].cell1 == posicaoAnterior) and (
                            self.problem.agent_search.pairs[j].cell2 == posicaoSeguinte)):                      #verifica se o pair corresponde à posição anterior e à posição seguinte
                        if(posicaoAnterior == self.problem.forklifts[forklift]):                                #verifica se é o primeiro passo do caminho do forklift
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[j].path
                        else:                                                                                   #caso contrário não guardamos para não ficarem passos repetidos
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[j].path[1:]
                        custo += self.problem.agent_search.pairs[j].value                                       # adicionamos o custo do pair ao custo anterior enquanto trabalharmos no mesmo forklift
                        posicaoAnterior = posicaoSeguinte                                                       #guardamos a posição seguinte como a posição anterior
                        break
                    if((self.problem.agent_search.pairs[j].cell2 == posicaoAnterior) and (
                            self.problem.agent_search.pairs[j].cell1 == posicaoSeguinte)):                      #verifica se o pair está guardado ao contrário
                        inverted_array = self.problem.agent_search.pairs[j].path[::-1]                          #inverte o array, uma vez que no path está guardado ao contrário (posição seguinte == cell1 e a posição anterior == cell2)
                        if (posicaoAnterior == self.problem.forklifts[forklift]):                               #verifica se é o primeiro passo do caminho do forklift
                            pathdoForklift = pathdoForklift + inverted_array
                        else:                                                                                   #caso contrário não guardamos para não ficarem passos repetidos
                            pathdoForklift = pathdoForklift + inverted_array[1:]
                        custo += self.problem.agent_search.pairs[j].value                                       # adicionamos o custo do pair ao custo anterior enquanto trabalharmos no mesmo forklift
                        posicaoAnterior = posicaoSeguinte                                                       #guardamos a posição seguinte como a posição anterior
                        break

            if (i + 1 == self.num_genes):                                                                       #verifica se estamos no ultimo produto ou forklift
                for l in reversed(range(len(self.problem.agent_search.pairs))):                                 #percorre o array pairs ao contrário para encontrar o pair que liga o ultimo produto à saida
                    if (((self.problem.agent_search.pairs[l].cell1 == posicaoAnterior) and (
                            self.problem.agent_search.pairs[l].cell2 == self.problem.agent_search.exit))):      #vamos ver qual é a posição no array pairs que corresponde ao ultimo produto e à saida
                        if (posicaoAnterior == self.problem.forklifts[forklift]):                               #verifica se é o primeiro passo do caminho do forklift
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[l].path
                        else:                                                                                   #caso contrário não guardamos para não ficarem passos repetidos
                            pathdoForklift = pathdoForklift + self.problem.agent_search.pairs[l].path[1:]
                        custo += self.problem.agent_search.pairs[l].value                                       # adicionamos o custo do ultimo par ao custo anterior
                        custoPorForklift.append(custo)                                                          # guardamos o custo do ultimo forklift no array de custos
                        Paths.append(pathdoForklift)                                                            #guardamos o path do forklift no array Paths, ou seja, o indice do forklift corresponde ao indice do seu caminho no array paths
                        break

        TamanhoCaminhos = []
        colisoes = 0
        for path in Paths:
            TamanhoCaminhos.append(len(path))
        if(len(TamanhoCaminhos) > 1):
            TamanhoCaminhosOrdenado = sorted(TamanhoCaminhos, reverse=True)
            segundoMaiorCaminho = TamanhoCaminhosOrdenado[1]

            for k in range(segundoMaiorCaminho):
                valid_paths = [path for path in Paths if k < len(path)]
                positions = [path[k] for path in valid_paths]
                if len(set(positions)) < len(positions):
                    colisoes += 1

            self.colisoes = colisoes
        else :
            self.colisoes = 0

        self.custoPorForklift = custoPorForklift
        steps = [len(path) for path in Paths]
        self.max_steps = max(steps) if steps else 0
        return Paths, self.max_steps, self.genome


    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"
        string += 'Colisoes: ' + str (self.colisoes) + "\n"
        string += 'Max Steps: ' + str (self.max_steps -1) + "\n"
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.colisoes = self.colisoes
        new_instance.max_steps = self.max_steps
        return new_instance