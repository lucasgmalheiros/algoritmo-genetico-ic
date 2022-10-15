import numpy as np
import pandas as pd
import glob
import subprocess
import re
import csv
import time

# Percorre cada uma das instâncias de teste e as resolve com todos os operadores de crossover

def natural_sort(array):
    """Recebe uma lista e a retorna ordenada para leitura humana"""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(array, key=alphanum_key)


def get_file_name(path):
    """Recebe o path de um arquivo no sistema e retorna apenas seu nome"""
    file_name = path.split('\\')[-1]
    return file_name


# Caminho das instâncias de tempos de processamento no sistema
instances = natural_sort(glob.glob('./tempos_processamento/*.txt'))

# Parâmetros fornecidos pelo irace
parameters = (['--operador {} --solucao 194 --geracao 133 --probabilidade 0.9'.format(n) for n in range(11)] +
              ['--operador 0 --solucao 194 --geracao 133 --probabilidade 0'])

# Criação do arquivo de makespan
with open('./analise_estatistica/crossover_operators.csv', 'w', newline='') as txt:
    writer = csv.writer(txt, delimiter=';')
    header = ['Instancia', 'OrderBased', 'PositionBased', 'PMX', 'OnePoint',
              'TwoPoint', 'TwoPointPermutation', 'OrderTwo', 'Linear',
              'SequenceBased', 'LoopBased', 'TwoCutPTL', 'NoCross', 'Otimo']
    writer.writerow(header)
    data = np.zeros(14, dtype=object)
    optimal_results = pd.read_csv('./analise_estatistica/optimal_solutions.csv',
                                  sep=';')['upper_bound']
    for i, file in enumerate(instances):
        file_name = get_file_name(file)
        data[0] = file_name
        data[-1] = str(optimal_results[i])
        start = time.time()
        for j, line in enumerate(parameters):
            commandline = ['ga_evolution.py', '--arquivo', file] + line.split()
            process = subprocess.run(commandline, stdout=subprocess.PIPE,
                                     shell=True, text=True)
            makespan = float(process.stdout)
            data[j + 1] = str(makespan)
        end = time.time()
        delta = end - start
        print(';'.join(data), 'Tempo no arquivo: {:.2f}s'.format(delta))
        writer.writerow(data)
