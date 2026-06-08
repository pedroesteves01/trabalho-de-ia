import inspect
from pathlib import Path
from typing import List, Tuple, Dict, Set
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np

import buscaClassica 

Estado = Tuple[int, int]

class LabirintoProblema:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.linhas = len(grid)
        self.colunas = len(grid[0]) if self.linhas > 0 else 0
        self.inicio = self._encontrar_sinal('A')
        self.objetivo = self._encontrar_sinal('B')

    def _encontrar_sinal(self, sinal: str) -> Estado:
        for r in range(self.linhas):
            for c in range(self.colunas):
                if self.grid[r][c] == sinal:
                    return (r, c)
        raise ValueError(f"Sinal '{sinal}' não foi encontrado no labirinto.")

    def vizinhos(self, estado: Estado) -> List[Tuple[str, Estado, float]]:
        r, c = estado
        movimentos = {
            'cima': (r - 1, c),
            'baixo': (r + 1, c),
            'esquerda': (r, c - 1),
            'direita': (r, c + 1)
        }
        validos = []
        for acao, (nr, nc) in movimentos.items():
            if 0 <= nr < self.linhas and 0 <= nc < self.colunas:
                if self.grid[nr][nc] != '#':
                    validos.append((acao, (nr, nc), 1.0))
        return validos

    def h(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    @staticmethod
    def reconstruir(no):
        estados = []
        acoes = []
        atual = no
        while atual.pai is not None:
            estados.append(atual.estado)
            acoes.append(atual.acao)
            atual = atual.pai
        estados.reverse()
        acoes.reverse()
        return estados, acoes


def ler_labirinto(caminho_arquivo: str) -> List[List[str]]:
    caminho = Path(caminho_arquivo)
    if caminho.suffix.lower() != ".txt":
        raise ValueError("Informe um arquivo com extensão .txt")
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with caminho.open("r", encoding="utf-8") as arquivo:
        linhas = [linha.rstrip("\n") for linha in arquivo if linha.strip()]
    return [list(linha) for linha in linhas]


# =============================================================================
# FUNÇÕES DE VISUALIZAÇÃO GRÁFICA (MATPLOTLIB)
# =============================================================================

def exibir_mapa_original_matplotlib(grid: List[List[str]], nome_arquivo: str):
    linhas = len(grid)
    colunas = len(grid[0])
    matriz_visual = np.zeros((linhas, colunas))
    
    pos_inicio = (0, 0)
    pos_objetivo = (0, 0)
    
    for r in range(linhas):
        for c in range(colunas):
            if grid[r][c] == '#':
                matriz_visual[r][c] = 1
            elif grid[r][c] == 'A':
                pos_inicio = (r, c)
            elif grid[r][c] == 'B':
                pos_objetivo = (r, c)
                
    matriz_visual[pos_inicio[0]][pos_inicio[1]] = 2
    matriz_visual[pos_objetivo[0]][pos_objetivo[1]] = 3

    cmap_custom = ListedColormap(['#FFFFFF', '#1A1A1A', '#2ECC71', '#E74C3C'])

    plt.figure(figsize=(7, 7))
    plt.imshow(matriz_visual, cmap=cmap_custom, vmin=0, vmax=3)
    
    plt.title(f"Mapa Original: {nome_arquivo}", fontsize=12, fontweight='bold')
    plt.xticks(range(colunas))
    plt.yticks(range(linhas))
    plt.grid(True, color='#7F8C8D', linestyle='-', linewidth=0.5)
    
    legend_elements = [
        Patch(facecolor='#1A1A1A', label='Parede (#)'),
        Patch(facecolor='#FFFFFF', label='Célula Livre'),
        Patch(facecolor='#2ECC71', label='Início (A)'),
        Patch(facecolor='#E74C3C', label='Objetivo (B)')
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    
    print("\n[Matplotlib] Exibindo janela com o mapa original. Feche a janela para continuar...")
    plt.show()


def exibir_resultado_matplotlib(problema: LabirintoProblema, resultado, nome_algoritmo: str):
    matriz_visual = np.zeros((problema.linhas, problema.colunas))
    
    for r in range(problema.linhas):
        for c in range(problema.colunas):
            if problema.grid[r][c] == '#':
                matriz_visual[r][c] = 1

    if resultado.sucesso and resultado.caminho:
        for (r, c) in resultado.caminho:
            matriz_visual[r][c] = 5
            
    ri, ci = problema.inicio
    rf, cf = problema.objetivo
    matriz_visual[ri][ci] = 2
    matriz_visual[rf][cf] = 3

    cmap_custom = ListedColormap(['#FFFFFF', '#1A1A1A', '#2ECC71', '#E74C3C', '#BDC3C7', '#3498DB'])

    plt.figure(figsize=(7, 7))
    plt.imshow(matriz_visual, cmap=cmap_custom, vmin=0, vmax=5)
    
    plt.title(f"Resultado da Busca - {nome_algoritmo}", fontsize=12, fontweight='bold')
    plt.xticks(range(problema.colunas))
    plt.yticks(range(problema.linhas))
    plt.grid(True, color='#7F8C8D', linestyle='-', linewidth=0.5)
    
    legend_elements = [
        Patch(facecolor='#1A1A1A', label='Parede (#)'),
        Patch(facecolor='#FFFFFF', label='Célula Livre'),
        Patch(facecolor='#2ECC71', label='Início (A)'),
        Patch(facecolor='#E74C3C', label='Objetivo (B)'),
        Patch(facecolor='#3498DB', label='Rota Encontrada')
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    
    nome_limpo = nome_algoritmo.lower().replace(' ', '_').replace('*', 'star')
    nome_arquivo = f"resultado_{nome_limpo}.png"
    plt.savefig(nome_arquivo, dpi=300)
    
    print(f"\n[Matplotlib] Exibindo janela com a rota. Imagem '{nome_arquivo}' salva em disco!")
    plt.show()


def exibir_grafico_desempenho_individual(resultado, valor_j):
    if not resultado.sucesso:
        print("\n[Matplotlib] O algoritmo não encontrou o caminho, gráfico de desempenho ignorado.")
        return

    plt.rcParams['figure.facecolor'] = '#F4F6F7'
    plt.rcParams['axes.facecolor'] = '#FFFFFF'

    metricas = ['Custo\n(Passos)', 'Nós\nExpandidos', 'Nós\nExplorados', 'Pico da\nFronteira']
    valores = [len(resultado.acoes), resultado.nos_expandidos, resultado.nos_explorados, resultado.max_fronteira]
    
    fig, ax = plt.subplots(figsize=(9, 5.5))
    
    cores = ['#2980B9', '#C0392B', '#8E44AD', '#F39C12']
    
    barras = ax.bar(metricas, valores, color=cores, edgecolor='#2C3E50', linewidth=1.5, alpha=0.9, width=0.5)
    
    tempo_ms = resultado.tempo_execucao * 1000
    info_text = (f"RAIO-X DO AGENTE\n\n"
                 f"Algoritmo: {resultado.algoritmo}\n"
                 f"Tempo: {tempo_ms:.2f} ms\n"
                 f"Utilidade (J): {valor_j:.2f}\n"
                 f"Status: Sucesso")
                 
    props = dict(boxstyle='round,pad=0.6', facecolor='#ECF0F1', edgecolor='#BDC3C7', alpha=0.9)
    ax.text(1.05, 0.5, info_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='center', bbox=props, weight='bold', color='#2C3E50')
    
    ax.set_title(f"Perfil de Desempenho Operacional: {resultado.algoritmo}", 
                 fontsize=14, weight='bold', color='#2C3E50', pad=15)
    ax.set_ylabel('Unidades Medidas', fontsize=11, weight='bold', color='#34495E')
    
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#BDC3C7')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f'{altura}',
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 5),  
                    textcoords="offset points",
                    ha='center', va='bottom', weight='bold', fontsize=11, color='#2C3E50')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.75) 
    
    nome_limpo = resultado.algoritmo.lower().replace(' ', '_').replace('*', 'star')
    nome_arquivo = f"grafico_metricas_{nome_limpo}.png"
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    
    print(f"[Matplotlib] Gráfico de métricas OTIMIZADO exportado: '{nome_arquivo}'")
    plt.show()


# =============================================================================
# FLUXO DE EXECUÇÃO PRINCIPAL
# =============================================================================

def listar_funcoes_busca_classica():
    funcoes = {
        nome: func
        for nome, func in inspect.getmembers(buscaClassica, inspect.isfunction)
        if nome.startswith("busca_") and nome != "busca_prioridade"
    }
    return funcoes


def escolher_funcao(funcoes):
    nomes = list(funcoes.keys())
    if not nomes:
        raise RuntimeError("Nenhuma função pública de busca encontrada em buscaClassica.py")

    print("\nFunções disponíveis em buscaClassica.py:")
    for i, nome in enumerate(nomes, start=1):
        print(f"{i}. {nome}")

    while True:
        escolha = input("Escolha o número da função de busca que deseja usar: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            return funcoes[nomes[int(escolha) - 1]], nomes[int(escolha) - 1]
        print("Opção inválida. Tente novamente.")


def main():
    caminho_input = input("Informe o caminho do arquivo .txt do labirinto: ").strip().strip('"')
    try:
        labirinto_matriz = ler_labirinto(caminho_input)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    nome_arquivo_limpo = Path(caminho_input).name

    exibir_mapa_original_matplotlib(labirinto_matriz, nome_arquivo_limpo)

    problema = LabirintoProblema(labirinto_matriz)
    funcoes = listar_funcoes_busca_classica()
    
    try:
        funcao_escolhida, nome_funcao = escolher_funcao(funcoes)
    except RuntimeError as e:
        print(e)
        return

    print(f"\nFunção selecionada: {nome_funcao}")
    print("Executando busca...")

    try:
        resultado = funcao_escolhida(problema)
        
        if resultado.sucesso:
            custo_caminho = len(resultado.acoes)
            passos = len(resultado.caminho)
            nos_expandidos = resultado.nos_expandidos
            
            valor_j = -((0.15 * custo_caminho) + (0.15 * nos_expandidos))
            j_print = f"{valor_j:.2f}"
            status = "Sim"
        else:
            custo_caminho = 0
            passos = 0
            nos_expandidos = resultado.nos_expandidos
            valor_j = -1000.0
            j_print = "-inf"
            status = "Não"

        print("\n" + "="*88)
        print(" TABELA DE RESULTADOS DA BUSCA".center(88))
        print("="*88)
        
        cabecalho = f"{'Algoritmo':<12} | {'Sucesso':<7} | {'Custo':<7} | {'Passos':<7} | {'Expandidos':<10} | {'Tempo (s)':<10} | {'Fronteira':<9}"
        linha = f"{resultado.algoritmo:<12} | {status:<7} | {custo_caminho:<7.1f} | {passos:<7} | {nos_expandidos:<10} | {resultado.tempo_execucao:<10.6f} | {resultado.max_fronteira:<9}"
        
        print(cabecalho)
        print("-" * 88)
        print(linha)
        print("="*88)
        print(f"Performance (Utilidade J): {j_print}")
        print("="*88)
        
        exibir_resultado_matplotlib(problema, resultado, resultado.algoritmo)
        
        if resultado.sucesso:
            exibir_grafico_desempenho_individual(resultado, valor_j)
        
    except Exception as e:
        print(f"Ocorreu um erro ao executar a função '{nome_funcao}': {e}")


if __name__ == "__main__":
    main()