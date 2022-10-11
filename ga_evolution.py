from ga_functions import *
from ga_operators import *
import argparse
import time

parser = argparse.ArgumentParser(description='Algoritmo genético')
parser.add_argument('-o', '--operador', type=int, help='Número de identificação do operador de crossover')
parser.add_argument('-a', '--arquivo', help='Nome do arquivo de tempos de processamento')
parser.add_argument('-s', '--solucao', type=int, help='Número de soluções em uma geração')
parser.add_argument('-g', '--geracao', type=int, help='Número de gerações no loop evolutivo')
parser.add_argument('-p', '--probabilidade', type=float, help='Probabilidade de crossover')
args = parser.parse_args()

# ------------------------------------------------------------------------------------------ #
o = args.operador  # Operador de crossover
f = args.arquivo  # Arquivo de tempos de processamento
n_solutions = args.solucao  # Número de soluções na primeira geração
n_generations = args.geracao  # Número de gerações no loop do GA
cp = args.probabilidade  # Probabilidade de crossover
# ------------------------------------------------------------------------------------------ #


def evolution(operator_n, file, n_sol, n_gen, cross_prob):
    """
    Recebe os parâmetros que definem a evolução das gerações e retorna o menor makespan obtido
    para um dado operador aplicado a uma matriz do arquivo em que são desenvolvidas n_gen gerações
    com n_sol soluções cada
    """
    start = time.time()
    # Setup
    # O número de soluções em uma geração não pode ser ímpar
    if (n_sol % 2) != 0:
        n_sol += 1
    # Tempos de processamento (arquivo)
    times_matrix = np.loadtxt(file, dtype=int)
    # Número de jobs
    n_jobs = len(times_matrix[0])
    # Geração inicial
    gen = generation_starter(n_jobs, n_sol)
    rank = generation_ranking(gen, times_matrix)
    # Determinação do operador de crossover
    operator = parser_operator(operator_n)
    op_name = operator.getName()
    # Evolução das gerações
    for i in range(n_gen):
        # Inicialização da nova geração
        new_gen = np.zeros(n_sol, dtype=np.ndarray)
        # Estratégia elitista
        new_gen[0], new_gen[1] = rank[0], rank[1]
        # Seleção dos pais
        gen_mksp = np.array([makespan(sol, times_matrix) for sol in rank])
        fitness = np.array(max(gen_mksp) - gen_mksp)
        s = prob_selection(rank, fitness)
        parent1, parent2 = s[0], s[1]
        c = 2  # Contador de soluções em uma geração
        # Loop de crossover
        while type(new_gen[-1]) == int:
            p = random.random()
            if p <= cross_prob:  # Caso o crossover seja realizado
                cross = operator.crossover(parent1, parent2)
                new_gen[c], new_gen[c + 1] = cross[0], cross[1]
                c += 2
            else:  # Caso o crossover não for realizado
                new_gen[c], new_gen[c + 1] = parent1, parent2
                c += 2
            # Nova seleção após cada reprodução
            s = prob_selection(rank, fitness)
            parent1, parent2 = s[0], s[1]
        # Ranking da nova geração
        rank = generation_ranking(new_gen, times_matrix)
    # Determinação da melhor solução
    best_solution = rank[0]
    mksp = makespan(best_solution, times_matrix)  # Makespan
    print(mksp)
    # Tempo de processamento
    # end = time.time()
    # delta = end - start
    # print('{:.4f}'.format(delta))
    return best_solution


if __name__ == '__main__':
    evolution(o, f, n_solutions, n_generations, cp)
