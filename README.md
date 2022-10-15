# Iniciação Científica

## Análise dos operadores de crossover em algoritmos genéticos aplicados a problemas de Flow Shop Scheduling

#### Códigos do projeto de iniciação científica desenvolvido por mim, Lucas Gabriel Malheiros, como bolsista do CNPq entre 08/2021 e 08/2022 sob orientação do Prof. Dr. Roberto Fernandes Tavares Neto, do Departamento de Engenharia de Produção da Universidade Federal de São Carlos.

A pesquisa teve como objetivo comparar o desempenho de operadores de crossover em [algoritmos genéticos](https://en.wikipedia.org/wiki/Genetic_algorithm)
aplicados à resolução de problemas de [*flowshop scheduling*](https://en.wikipedia.org/wiki/Flow-shop_scheduling) permutacionais. Para determinar os operadores de
crossover a serem implementados, foram pesquisados artigos na base da CAPES considerando
trabalhos publicados nos últimos dois anos. A partir desses artigos, selecionamos os operadores
mais utilizados. Foram selecionados os 11 seguintes operadores: order-based, position-based,
partially-mapped (PMX), one-point, two-point, two-point permutation (two-point crossover 2),
order crossover 2 (OX2), linear, sequence-based, loop-based e two-cut PTL.

O algoritmo genético, desenvolvido em Python, tem como objetivo minimizar o [makespan](https://en.wikipedia.org/wiki/Makespan) 
e suporta todos os operadores de crossover supracitados, além de utilizar um operador de 
[*roulette-wheel selection*](https://en.wikipedia.org/wiki/Fitness_proportionate_selection). Entretanto, 
não foi implementado operador de mutação, que pode ser desenvolvido para melhorar ainda mais o desempenho do algoritmo. Para validação do algoritmo, foram utilizadas
as instâncias de teste de *Flow shop sequencing*, disponíveis em http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html, e que são
acessadas em [tempos_processamento](https://github.com/lucasgabriel21/iniciacao-cientifica/tree/master/tempos_processamento).

## Arquivos

### [ga_operators.py](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/ga_operators.py)

Contém implementação de todos os operadores de crossover.

### [ga_functions.py](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/ga_functions.py)

Funcionalidades básicas do algoritmo genético.

### [ga_evolution.py](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/ga_evolution.py)

Configuração de chamada por linha de comando e função de evolução, que aplica os procedimentos do algoritmo genético 
às possíveis soluções do problema.

### [runall.py](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/runall.py)

Definidos o número de soluções, número de gerações e probabilidade de crossover, realiza o chamado de *ga_evolution.py* para todos
os arquivos de tempos de processamento aplicados a todos os operadores de crossover e salva os makespan resultantes em um arquivo csv.

### [analise_estatistica](https://github.com/lucasgabriel21/iniciacao-cientifica/tree/master/analise_estatistica)

A pasta contém todos os dados de makespan gerados no formato **crossover_operators_{numero de solucoes}_{numero de geracoes}.csv**. Comparando com as melhores 
soluções conhecidas, salvas em [optimal_solutions.csv](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/analise_estatistica/optimal_solutions.csv),
o notebook [analise_crossover.ipynb](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/analise_estatistica/analise_crossover.ipynb)
apresenta a diferença entre os operadores de crossover em relação ao erro relativo por meio de boxplots. 

Ainda há a análise do tempo computacional de cada um desses operadores, conforme os dados de 
[crossover_operators_time.csv](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/analise_estatistica/crossover_operators_time.csv), para
gerar a tabela de Excel [times.xlsx](https://github.com/lucasgabriel21/iniciacao-cientifica/blob/master/analise_estatistica/times.xlsx).
