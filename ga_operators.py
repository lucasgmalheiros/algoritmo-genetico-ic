import numpy as np
import random

# Operadores de crossover

# 0
class OrderBasedCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        Esse operador de crossover é implementado transferindo uma sequência ordenada de genes (string),
        escolhida aleatoriamente, a partir do cromossomo de um dos pais, preservando as mesmas posições,
        para o cromossomo da criança, a solução filha. Os genes faltantes são preenchidos na solução filha
        na mesma ordem em que aparecem no cromossomo do outro pai. Retorna duas offspring como solução.
        Os pais podem ter pontos de corte diferentes para evitar o mesmo resultado que o two-point crossover.
        """
        size = len(p1)
        # Definição de pontos de corte aleatórios para p1 e p2
        slice_p1 = np.sort(np.array(random.sample(range(1, size - 1), 2)))
        slice_p2 = np.sort(np.array(random.sample(range(1, size - 1), 2)))
        # print('Slice p1:', slice_p1)
        # print('Slice p2:', slice_p2)
        cut_1_p1, cut_2_p1 = slice_p1[0] - 1, slice_p1[1]  # Cortes de p1
        cut_1_p2, cut_2_p2 = slice_p2[0] - 1, slice_p2[1]  # Cortes de p2
        cut_region_p1 = range(cut_1_p1, cut_2_p1)
        cut_region_p2 = range(cut_1_p2, cut_2_p2)
        # Inicializa as offspring como arrays de zeros
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópia dos pais sem os elementos da região de corte do outro
        p1_c = np.array([e for e in p1 if e not in p2[cut_1_p2:cut_2_p2]])
        p2_c = np.array([e for e in p2 if e not in p1[cut_1_p1:cut_2_p1]])
        m, n = 0, 0  # Indicadores de posições para os cromossomos de cópia
        # Gerando s offspring
        for i in range(size):
            if i in cut_region_p1:  # Transfere os elementos das regiões de corte
                off2[i] = p1[i]
            else:  # Preenche os elementos faltantes
                off2[i] = p2_c[n]
                n += 1
            if i in cut_region_p2:  # Transfere os elementos das regiões de corte
                off1[i] = p2[i]
            else:  # Preenche os elementos faltantes
                off1[i] = p1_c[m]
                m += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 1
class PositionBasedCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        É selecionado um conjunto aleatório de posições,
        correspondentes às informações genéticas dos pais
        que serão transferidas diretamente para uma solução filha.
        Os genes faltantes são preenchidos conforme aparecem no cromossomo do outro pai.
        Retorna duas offspring como solução.
        """
        size = len(p1)
        # Gerando as posições aleatórias
        n_positions = random.randint(1, size - 2)  # Número de posições aleatória
        # n_positions = size//2  # Número de posições fixas
        positions = np.sort(np.array(random.sample(range(size), n_positions)))
        # print('Positions:', [p + 1 for p in positions])
        # Inicializa as offspring como arrays de zeros
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópias dos pais com os elementos faltantes
        p1_c = np.array([e for e in p1 if e not in [p2[i] for i in positions]])
        p2_c = np.array([e for e in p2 if e not in [p1[i] for i in positions]])
        n = 0
        # Criando as offspring
        for i in range(size):
            # Preenchendo os elementos das posições selecionadas
            if i in positions:
                off1[i] = p2[i]
                off2[i] = p1[i]
            # Preenchendo os elementos restantes conforme aparecem no outro pai
            else:
                off1[i] = p1_c[n]
                off2[i] = p2_c[n]
                n += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 2
class PMXCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        O procedimento inicia-se com a definição aleatória de dois pontos de corte para as soluções pai.
        Elementos entre os cortes nos cromossomos pais com mesma posição são então mapeados,
        cria-se uma correspondência entre eles. Sejam off1 e off2 duas soluções filhas idênticas aos pais p1 e p2,
        respectivamente, off1 receberá a informação correspondente às posições entre os cortes de p2,
        e os genes repetidos em off1 serão trocados de acordo com op mapeamento da etapa anterior.
        O procedimento para geração da solução off2 é análogo.
        """
        size = len(p1)
        # Seleção de pontos aleatórios de corte
        cut_points = np.sort(np.array(random.sample(range(2, size), 2)))
        # print('Cut region:', cut_points)
        cut_1, cut_2 = cut_points[0] - 1, cut_points[1]
        cut_region = range(cut_1, cut_2)
        # Inicializa as offspring como cópias dos pais
        off1 = np.copy(p1)
        off2 = np.copy(p2)
        # Mapeamento dos elementos das regiões de corte
        p1_cut = np.array(p1[cut_1:cut_2])
        p2_cut = np.array(p2[cut_1:cut_2])
        mapping = tuple((zip(p1_cut, p2_cut)))
        # Criando as offspring
        for i in range(size):
            # Transferindo os elementos da região de corte
            if i in cut_region:
                off1[i] = p2[i]
                off2[i] = p1[i]
            # Usando os valores mapeados para substituir genes repetidos
            else:
                while off1[i] in p2_cut:
                    for t in range(len(mapping)):
                        if off1[i] == mapping[t][1]:
                            off1[i] = mapping[t][0]
                while off2[i] in p1_cut:
                    for t in range(len(mapping)):
                        if off2[i] == mapping[t][0]:
                            off2[i] = mapping[t][1]
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 3
class OnePointCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        É um operador simples que consiste em dividir os cromossomos pai em um ponto
        definido aleatoriamente para então gerar novas soluções recombinando as partes.
        A informação transferida por um pai vai do início do seu array até o ponto de corte,
        e os genes restantes são preenchidos conforme aparecem no outro pai.
        """
        size = len(p1)
        # Seleção de um ponto de corte aleatório
        cut_point = random.randint(1, size - 2)
        cut_region = range(cut_point)
        # print('Cut point:', cut_point)
        # Inicializa as offspring como arrays de zeros
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópias dos pais sem os elementos da região de corte do outro
        p1_c = np.array([e for e in p1 if e not in p2[:cut_point]])
        p2_c = np.array([e for e in p2 if e not in p1[:cut_point]])
        n = 0
        # Criando as offspring
        for i in range(size):
            # Transferindo os elementos da região de corte
            if i in cut_region:
                off1[i] = p2[i]
                off2[i] = p1[i]
            # Preenchendo os elementos faltantes conforme aparecem no outro pai
            else:
                off1[i] = p1_c[n]
                off2[i] = p2_c[n]
                n += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 4
class TwoPointCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        São determinados aleatoriamente dois pontos de corte para os cromossomos de ambos os pais,
        as informações entre os dois pontos de corte são transferidas para as offspring.
        Os genes restantes são preenchidos conforme aparecem no outro pai.
        """
        size = len(p1)
        # Seleção dos dois pontos de corte aleatórios
        cut_points = np.sort(np.array(random.sample(range(2, size), 2)))
        # print('Cut region:', cut_points)
        cut_1, cut_2 = cut_points[0] - 1, cut_points[1]
        cut_region = range(cut_1, cut_2)
        # Inicializa as offspring como arrays de zeros
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópias dos pais sem os elementos da região de corte do outro
        p1_c = np.array([e for e in p1 if e not in p2[cut_1:cut_2]])
        p2_c = np.array([e for e in p2 if e not in p1[cut_1:cut_2]])
        n = 0
        # Criando a offspring
        for i in range(size):
            # Transferindo os elementos da região de corte
            if i in cut_region:
                off1[i] = p2[i]
                off2[i] = p1[i]
            # Preenchendo os elementos faltantes conforme aparecem no outro pai
            else:
                off1[i] = p1_c[n]
                off2[i] = p2_c[n]
                n += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 5
class TwoPointPermutationCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        Essa variação do two-point crossover transmite os genes nas posições exteriores aos cortes, extremos do
        cromossomo de um dos pais, e preenche as informações faltantes conforme aparecem no outro pai.
        """
        size = len(p1)
        # Seleção dos dois pontos de corte aleatórios
        cut_points = np.sort(np.array(random.sample(range(2, size), 2)))
        # print('Cut region:', cut_points)
        cut_1, cut_2 = cut_points[0] - 1, cut_points[1]
        cut_region = range(cut_1, cut_2)
        # Inicializa as offspring como arrays de zeross
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópias dos pais sem os elementos da região de corte do outro
        p1_c = np.array([e for e in p1 if e in p2[cut_1:cut_2]])
        p2_c = np.array([e for e in p2 if e in p1[cut_1:cut_2]])
        n = 0
        # # Criando a offspring
        for i in range(size):
            # Transferindo os jobs nos extremos do cromossomo (fora da região de corte)
            if i not in cut_region:
                off1[i] = p2[i]
                off2[i] = p1[i]
            # Preenchendo os jobs do centro conforme aparecem no outro pai
            else:
                off1[i] = p1_c[n]
                off2[i] = p2_c[n]
                n += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 6
class OrderTwoCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        São determinadas duas sequências ordenadas de genes que serão transferidas diretamente de uma solução pai
        para uma filha. A primeira sequência vai do início do cromossomo até o primeiro ponto de parada,
        escolhido aleatoriamente, a segunda sequência vai do segundo ponto até o final do cromossomo. Os genes
        faltantes, que ficarão nas posições entre os dois pontos, são então preenchidos conforme aparecem no outro pai.
        Os pais podem ter pontos de corte diferentes para evitar o mesmo resultado que o two-point crossover II.
        """
        size = len(p1)
        # Pontos de corte aleatórios para p1 e p2
        slice_p1 = np.sort(np.array(random.sample(range(1, size - 1), 2)))
        slice_p2 = np.sort(np.array(random.sample(range(1, size - 1), 2)))
        # print('Slice p1:', slice_p1)
        # print('Slice p2:', slice_p2)
        cut_1_p1, cut_2_p1 = slice_p1[0] - 1, slice_p1[1]  # Corte de p1
        cut_1_p2, cut_2_p2 = slice_p2[0] - 1, slice_p2[1]  # Corte de p2
        cut_region_p1 = range(cut_1_p1, cut_2_p1)
        cut_region_p2 = range(cut_1_p2, cut_2_p2)
        # Inicializa as offspring como arrays de zeross
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Cópias dos pais somente com os elementos da região de corte do outro
        p1_c = np.array([e for e in p1 if e in p2[cut_1_p2:cut_2_p2]])
        p2_c = np.array([e for e in p2 if e in p1[cut_1_p1:cut_2_p1]])
        m, n = 0, 0
        # Criando a offspring
        for i in range(size):
            if i not in cut_region_p1:  # Transfere os elementos fora da região de corte
                off2[i] = p1[i]
            else:  # Preenche os elementos centrais restantes
                off2[i] = p2_c[n]
                n += 1
            if i not in cut_region_p2:  # Transfere os elementos fora da região de corte
                off1[i] = p2[i]
            else:  # Preenche os elementos centrais restantes
                off1[i] = p1_c[m]
                m += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 7
class LinearCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        Nesse operador as soluções filhas off1 e off2 são inicializadas como cópias dos pais p1 e p2, respectivamente.
        São determinados dois pontos de corte aplicados aos cromossomos pai, os elementos entre os dois pontos
        de corte do pai p1 são removidos da solução off2 e então reinseridos na mesma ordem que estão em p1.
        O mesmo procedimento é feito para a geração da solução off1 a partir de p2.
        """
        size = len(p1)
        # Seleção dos pontos de corte aleatórios
        cut_points = np.sort(np.array(random.sample(range(2, size), 2)))
        # print('Cut region:', cut_points)
        cut_1, cut_2 = cut_points[0] - 1, cut_points[1]
        # Inicializa as offspring como cópias de p1 e p2
        off1 = np.copy(p1)
        off2 = np.copy(p2)
        # Arrays apenas com elementos da região de corte
        p1_c = np.array([e for e in p1[cut_1:cut_2]])
        p2_c = np.array([e for e in p2[cut_1:cut_2]])
        n, m = 0, 0
        # Criando a offspring
        for i in range(size):
            if off2[i] in p1[cut_1:cut_2]:  # Troca os elementos conforme aparecem no corte de p1
                off2[i] = p1_c[n]
                n += 1
            if off1[i] in p2[cut_1:cut_2]:  # Troca os elementos conforme aparecem no corte de p2
                off1[i] = p2_c[m]
                m += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 8
class SequenceBasedCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        Seleciona-se metade dos genes do pai p1 aleatoriamente e os ordena de acordo com a ordem ocorrência.
        Esses genes também são localizados no pai p2 e ordenados de acordo com a ocorrência. Para geração das
        soluções filhas é feito o crossover desses genes selecionados conforme o mapeamento de suas posições em p1 e p2.
        """
        size = len(p1)
        # Seleção aleatória de metade dos elementos de p1
        positions = np.sort(np.array(random.sample(range(size), size // 2)))
        # print('Positions in p1: {}'.format(positions + 1))
        # Inicializa as offspring como cópias dos pais
        off1 = np.copy(p1)
        off2 = np.copy(p2)
        # Mapeando os elementos de p1 selecionados
        p1_g = [p1[i] for i in positions]  # Array com os elementos conforme aparecem em p1
        p2_g = [e for e in p2 if e in p1_g]  # Array com os elementos conforme aparecem em p2
        mapping = tuple((zip(p1_g, p2_g)))  # Tupla para mapear os elementos das arrays p1_g e p2_g
        # Criando a offspring
        for i in range(size):
            if off1[i] in p1_g:  # Troca os elementos conforme aparecem em p2
                off1[i] = mapping[p1_g.index(off1[i])][1]
            if off2[i] in p2_g:  # Troca os elementos conforme aparecem em p1
                off2[i] = mapping[p2_g.index(off2[i])][0]
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 9
class LoopBasedCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        Inicializam-se uma variável de posição j em 0 e uma array de posições vazia k. Enquanto o gene na posição j
        em p2 for diferente do primeiro gene de p1, j recebe a posição do gene em p1 correspondente ao gene de
        posição j em p2. Os valores atualizados de j vão sendo armazenados na fila k. Por fim a formação da off1
        ocorre recebendo os genes das posições contidas em k de p1, e no restante das posições recebe os elementos de
        p2. Analogamente ocorre a formação da outra solução.
        """
        size = len(p1)
        # Loop
        j = 0  # Variável de posição
        k = np.array([], dtype=int)  # Array de posições
        while p2[j] != p1[0]:  # Enquanto op gene de posição j em p2 for diferente do primeiro gene de p1
            j = np.where(p1 == p2[j])  # j recebe a posição do gene em p1 que corresponde ao gene de posição j em p2
            k = np.append(k, j)  # j é armazenado na fila
        k = np.sort(np.append(k, 0))  # k recebe op valor correspondente à posição inicial (0) e é ordenada
        # print('Positions:', k + 1)
        # Inicialização das offspring como cópias dos pais
        off1 = np.copy(p2)
        off2 = np.copy(p1)
        n = 0
        # Criação das offspring
        for i in range(size):
            if i in k:
                off1[i] = p1[k[n]]  # off1 recebe os genes das posições contidas em k de p1
                off2[i] = p2[k[n]]  # off2 recebe os genes das posições contidas em k de p2
                n += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__

# 10
class TwoCutPTLCrossover:
    @staticmethod
    def crossover(p1, p2):
        """
        São determinados dois pontos aleatórios de corte no cromossomo p1, a informação entre os cortes
        é movida para o canto direito (final) da filha off1 e para o canto esquerdo (início) de off2,
        os genes faltantes são preenchidos conforme aparecem em p2.
        """
        size = len(p1)
        # Seleção dos pontos de corte aleatórios
        cut_points = np.sort(np.array(random.sample(range(2, size), 2)))
        # print('Cut region: ', cut_points)
        cut_1, cut_2 = cut_points[0] - 1, cut_points[1]
        # Iniciando as offspring como arrays de zeros
        off1 = np.zeros(size, dtype=int)
        off2 = np.zeros(size, dtype=int)
        # Array com os genes entre os cortes de p1
        p1_c = np.array([e for e in p1 if e in p1[cut_1:cut_2]])
        # Removendo os genes entre os cortes de p1 do pai p2
        p2_c = np.array([e for e in p2 if e not in p1[cut_1:cut_2]])
        n, m = 0, 0
        # Criando as offspring
        for i in range(size):
            # Para off1 os genes da região de corte de p1 são inserido ao final do cromossomo
            if i < (size - len(p1_c)):
                off1[i] = p2_c[i]
            else:
                off1[i] = p1_c[n]
                n += 1
            # Em off2 os genes da região de corte de p1 são inserido no início do cromossomo
            if i < len(p1_c):
                off2[i] = p1_c[i]
            else:
                off2[i] = p2_c[m]
                m += 1
        # Checagem de validade das offspring
        assert all(job in off1 for job in range(size)) and \
               all(job in off2 for job in range(size))
        return off1, off2

    def getName(self):
        return self.__class__.__name__


def parser_operator(op):
    """Seleciona um operador de crossover a partir do input por linha de comando"""
    if op == 0:
        operator = OrderBasedCrossover()
    elif op == 1:
        operator = PositionBasedCrossover()
    elif op == 2:
        operator = PMXCrossover()
    elif op == 3:
        operator = OnePointCrossover()
    elif op == 4:
        operator = TwoPointCrossover()
    elif op == 5:
        operator = TwoPointPermutationCrossover()
    elif op == 6:
        operator = OrderTwoCrossover()
    elif op == 7:
        operator = LinearCrossover()
    elif op == 8:
        operator = SequenceBasedCrossover()
    elif op == 9:
        operator = LoopBasedCrossover()
    elif op == 10:
        operator = TwoCutPTLCrossover()
    else:
        raise ValueError('O operador selecionado não existe!')
    return operator
