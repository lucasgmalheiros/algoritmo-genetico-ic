# Iniciação Científica

## Análise dos operadores de crossover em algoritmos genéticos aplicados a problemas de Flow Shop Scheduling

#### Códigos do projeto de iniciação científica desenvolvido por mim, [Lucas Gabriel Malheiros](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K9970734E8&tokenCaptchar=03AIIukzhCjRMAgpFqj3YzXGcDPbImjUe-ie-vcP0Q5IU4iI6JlOJgVpVBC7_zG6Y4m7YkU_GRo5wyfmzR2SADdDzJHqnA-aPzNDaNCqUjltFQHNxpyb2PrsQRjhy1-RnxFQT9JFSK_C_NE0ofcjyFUVwXqJ2r9ie9RA7ps4toHb5YnzNt_07Z8brFybu7779SC4PjU1b9r9NWAQknSl2qZ7UG9CDqcy99AAJEuBR8IgUMT3tS2iwnTY8edFRw40k0lQEdULIcftXxaws1Apyxzp0e118-1McNj_Ij4KUm75kLnyLqhd-d_yxE9VIIFNw0swnhppFLHY9otIYddOAERK1g9vArgijRAdRj8hpMJcQV8fT-OfsH1Kdgh8oYR-99DCHMrXJAdjmJQ8pcxYlBa-LJIdUKs0noaTygRhXfyX3jOX4EUIVtQ04WG2lsx_K-Nu3hHGaartR0fys2VRWfIWSlBnxoTlO9fOhPqaSTUHdjA69Xsix8wS7o4Ti99U5jsxWnMBBWBn5Tl9SianXfq7-LylQrkLf2gQ), como bolsista do CNPq entre 08/2021 e 08/2022 sob orientação do Prof. Dr. [Roberto Fernandes Tavares Neto](https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4770875A8&tokenCaptchar=03AIIukzj8pEtMzCLhnMRw7vz9PAj9zwYoHSS7sO3ASZNKGie83pHOG54ffgCvUA5Q18TseXcwz2HQy1rvxs0eWQjP3sWfm8eOLtu5JlaHsWSe9DUivLgAKrlFswwjGuXtcVG-sqIG4EYy4hii76SWnLcziwOY_FTalIBzf1XASmpWDNYrQFkmDHewYjsjvOgroQYmft6F7e0DNDi9io5gqrSGnyI52NFFLmQzA5EARLXsIYJkHP6DJ16jnIKsLBJC9Xb9WTw5bnoZNiiFCgClFZ-NOAEXkpwi5hUhcQ44NoTGs8uCivLRzFjmCMpm6IRyWNEewV16gcXAKksHUZKDxt8tcqw7GooIohf_QbNSYluAdUWJ3D6o0W7p86oL0cuMSb_f-sD6wwMfYhV_8xziNyOfYU7p5u5132QPHgLmxuNs4NYQnEAy_R6xTtd7gGxpmHgHwz_7Y_KfhkzEFP1Gfgefc9iESIrp4IXMReqU0O1wsqM-2ORrP5QkZXQt6d6hP-PQpYz_NeGmwtAJ3wWtrHu60eTdqxm2gw), do Departamento de Engenharia de Produção ([DEP](https://dep.ufscar.br/)) da Universidade Federal de São Carlos ([UFSCar](https://www.ufscar.br/)).

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
