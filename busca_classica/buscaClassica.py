import math
import heapq
import time
import itertools
from collections import deque
from typing import List, Optional, Tuple, Set, Dict, NamedTuple

# =============================================================================
# DEFINIÇÃO DE ESTRUTURAS DE DADOS E TIPOS
# =============================================================================

Estado = Tuple[int, int] 

class No:
    def __init__(self, estado: Estado, pai=None, acao: Optional[str] = None, g: float = 0.0):
        self.estado = estado
        self.pai = pai
        self.acao = acao  
        self.g = g

    def __lt__(self, other):
        return self.g < other.g

class ResultadoBusca(NamedTuple):
    algoritmo: str
    sucesso: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    max_fronteira: int
    tempo_execucao: float

def busca_largura(self) -> ResultadoBusca:
    tempo_ini = time.time()
    inicio = No(self.inicio)
    fronteira = deque([inicio])
    em_fronteira = {self.inicio}
    explorados: Set[Estado] = set()
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1

    while fronteira:
        max_fronteira = max(max_fronteira, len(fronteira))
        no = fronteira.popleft()
        em_fronteira.remove(no.estado)
        nos_explorados += 1

        if no.estado == self.objetivo:
            caminho, acoes = self.reconstruir(no)
            return ResultadoBusca('BFS', True, caminho, acoes, nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)

        explorados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in self.vizinhos(no.estado):
            if estado not in explorados and estado not in em_fronteira:
                filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                fronteira.append(filho)
                em_fronteira.add(estado)

    return ResultadoBusca('BFS', False, [], [], nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)


def busca_profundidade(self) -> ResultadoBusca:
    tempo_ini = time.time()
    inicio = No(self.inicio)
    fronteira = [inicio]
    em_fronteira = {self.inicio}
    explorados: Set[Estado] = set()
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1

    while fronteira:
        max_fronteira = max(max_fronteira, len(fronteira))
        no = fronteira.pop()
        em_fronteira.remove(no.estado)
        nos_explorados += 1

        if no.estado == self.objetivo:
            caminho, acoes = self.reconstruir(no)
            return ResultadoBusca('DFS', True, caminho, acoes, nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)

        explorados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in self.vizinhos(no.estado):
            if estado not in explorados and estado not in em_fronteira:
                filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                fronteira.append(filho)
                em_fronteira.add(estado)

    return ResultadoBusca('DFS', False, [], [], nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)


def busca_prioridade(self, nome: str, funcao_prioridade) -> ResultadoBusca:
    tempo_ini = time.time()
    contador = itertools.count()
    inicio = No(self.inicio, g=0.0)
    fronteira = []
    heapq.heappush(fronteira, (funcao_prioridade(inicio), next(contador), inicio))
    melhor_g: Dict[Estado, float] = {self.inicio: 0.0}
    fechados: Set[Estado] = set()
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1

    while fronteira:
        max_fronteira = max(max_fronteira, len(fronteira))
        _, _, no = heapq.heappop(fronteira)

        if no.estado in fechados:
            continue

        nos_explorados += 1

        if no.estado == self.objetivo:
            caminho, acoes = self.reconstruir(no)
            return ResultadoBusca(nome, True, caminho, acoes, nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)

        fechados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in self.vizinhos(no.estado):
            novo_g = no.g + custo
            if estado in fechados:
                continue
            if novo_g < melhor_g.get(estado, math.inf):
                filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                melhor_g[estado] = novo_g
                heapq.heappush(fronteira, (funcao_prioridade(filho), next(contador), filho))

    return ResultadoBusca(nome, False, [], [], nos_explorados, nos_expandidos, max_fronteira, time.time() - tempo_ini)


def busca_custo_uniforme(self) -> ResultadoBusca:
    return busca_prioridade(self, 'UCS', lambda no: no.g)


def busca_gulosa(self) -> ResultadoBusca:
    return busca_prioridade(self, 'Gulosa', lambda no: self.h(no.estado))


def busca_astar(self) -> ResultadoBusca:
    return busca_prioridade(self, 'A*', lambda no: no.g + 1.0 * self.h(no.estado))