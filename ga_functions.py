import numpy as np
import re

# Funções do algoritmo genético

def generation_starter(num_jobs, num_arrays):
    """
    Inicializa a primeira geração com o número de soluções dado por num_arrays.
    Cada solução é uma permutação do número de jobs (num_jobs).
    Retorna um array com todas as soluções iniciais.
    """
    # Array para armazenar as soluções da 1ª geração
    generation = np.zeros(num_arrays, dtype=np.ndarray)
    # A solução é criada como uma array de permutação aleatória dos jobs
    for i in range(num_arrays):
        generation[i] = np.random.permutation(num_jobs)
    return generation


def makespan(solution, processing_times):
    """Dadas uma solução e uma matriz de tempos de processamento, retorna o valor do makespan"""
    # Array de zeros para armazenar os completion times
    completion_times = np.zeros(processing_times.shape)
    # Avalia os completion time em cada máquina
    for machine in range(len(processing_times)):
        # Associa uma posição 'p' para avaliar cada job da solução
        for p, job in enumerate(solution):
            # Preenchendo a primeira linha de completion times
            if machine == 0:
                completion_times[machine, job] = (completion_times[machine, solution[p - 1]]
                                                  + processing_times[machine, job])
            # Preenchendo a coluna do primeiro job
            elif p == 0:
                completion_times[machine, job] = (completion_times[machine - 1, solution[p]]
                                                  + processing_times[machine, job])
            # Preenchendo o resto dos completion times
            else:
                completion_times[machine, job] = (max(completion_times[machine - 1, solution[p]],
                                                      completion_times[machine, solution[p - 1]])
                                                  + processing_times[machine, job])
    # O makespan é o maior valor da array de completion times
    mksp = np.amax(completion_times)
    return mksp


def generation_ranking(generation, processing_times):
    """Retorna um rankeamento de uma dada geração conforme o critério de minimização do makespan,
    feito em ordem crescente, a solução de menor makespan da geração é colocada na primeira posição"""
    gen = np.copy(generation)
    gen_makespan = np.array([makespan(sol, processing_times) for sol in gen])
    # Associa uma solução com o seu makespan
    for n in range(len(gen)):
        gen[n] = gen[n], gen_makespan[n]
    # Ordenando conforme o valor de makespan
    sorted_gen = np.asarray(sorted(gen, key=lambda x: x[1]), dtype=object)
    # Remove a informação do makespan e retorna uma array de soluções rankeadas
    rank = np.array([s[0] for s in sorted_gen])
    return rank


def natural_sort(array):
    """Recebe uma lista e a retorna ordenada para leitura humana"""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(array, key=alphanum_key)


def get_file_name(path):
    """Recebe o path de um arquivo no sistema e retorna apenas o seu nome"""
    file_name = path.split('/')[-1]
    return file_name


def prob_selection(generation, fitness):
    """
    Recebe uma geração de soluções e realiza a seleção de pais de acordo
    com uma probabilidade de seleção. Quanto menor o makespan, maior a
    chance da solução ser selecionada
    """
    if sum(fitness) == 0:  # Distribuição uniforme
        rel_fit = np.full(len(fitness), 1/len(fitness))
    else:  # Probabilidade de seleção proporcional
        rel_fit = np.array(fitness/sum(fitness))
    prob = np.array([sum(rel_fit[:i+1]) for i in range(len(rel_fit))])
    parents = np.zeros(2, dtype=np.ndarray)
    for i in range(len(parents)):
        r = np.random.random()
        for n in range(len(generation)):
            if 0 <= r <= prob[0]:
                parents[i] = generation[0]
            elif prob[n] <= r <= prob[n+1]:
                parents[i] = generation[n+1]
    return parents
