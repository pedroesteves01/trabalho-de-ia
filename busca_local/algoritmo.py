import random
import math
import heapq
import time
import matplotlib.pyplot as plt
import numpy as np

def ler_labirinto_e_limpar(nome_arquivo):
    labirinto = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha_limpa = linha.replace('\n', '').replace('\r', '')
            if linha_limpa:
                labirinto.append(list(linha_limpa))
            
    largura_maxima = max(len(linha) for linha in labirinto)
    for i in range(len(labirinto)):
        if len(labirinto[i]) < largura_maxima:
            falta = largura_maxima - len(labirinto[i])
            labirinto[i].extend(['#'] * falta)
            
    checkpoints_brutos = {}
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i]) - 1):
            if labirinto[i][j] == 'C' and labirinto[i][j+1].isdigit():
                nome_cp = 'C' + labirinto[i][j+1]
                checkpoints_brutos[nome_cp] = (i, j)
                
    for nome_cp, (i, j) in checkpoints_brutos.items():
        labirinto[i][j] = ' '
        labirinto[i][j+1] = ' '

    def encontrar_posicao_caractere(mapa, simbolo):
        for r, linha in enumerate(mapa):
            for c, v in enumerate(linha):
                if v == simbolo:
                    return (r, c)
        return None

    inicio_raw = encontrar_posicao_caractere(labirinto, 'A')
    objetivo_raw = encontrar_posicao_caractere(mapa=labirinto, simbolo='B')

    if inicio_raw: labirinto[inicio_raw[0]][inicio_raw[1]] = ' '
    if objetivo_raw: labirinto[objetivo_raw[0]][objetivo_raw[1]] = ' '

    # AJUSTE INTELIGENTE: Garante que nenhum ponto comece preso dentro de uma parede '#'
    def garantir_ponto_livre(mapa, ponto):
        r, c = ponto
        if mapa[r][c] == ' ':
            return (r, c)
        # Se cair em parede, busca o vizinho livre mais próximo nas 4 direções
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nr][nc] == ' ':
                return (nr, nc)
        return (r, c)

    checkpoints_limpos = {}
    for nome, pos in checkpoints_brutos.items():
        checkpoints_limpos[nome] = garantir_ponto_livre(labirinto, pos)

    inicio_ajustado = garantir_ponto_livre(labirinto, inicio_raw) if inicio_raw else None
    objetivo_ajustado = garantir_ponto_livre(labirinto, objetivo_raw) if objetivo_raw else None
        
    return labirinto, checkpoints_limpos, inicio_ajustado, objetivo_ajustado, checkpoints_brutos, inicio_raw, objetivo_raw

lab, checkpoints_dict, inicio, objetivo, pos_originais_cps, inicio_orig, obj_orig = ler_labirinto_e_limpar('./lab2.txt')

posicoes_originais = {'A': inicio_orig, 'B': obj_orig}
for k, v in pos_originais_cps.items():
    posicoes_originais[k] = v

alvos = list(checkpoints_dict.values())

if not alvos or inicio is None or objetivo is None:
    raise ValueError("Erro Crítico: Elementos fundamentais (A, B ou C's) não foram identificados. Cheque o arquivo lab2.txt.")

def ucs_caminho_exato(labirinto, inicio_ponto, fim_ponto):
    fila = [(0, inicio_ponto, [inicio_ponto])]
    visitados = set()

    while fila:
        custo, (x, y), caminho = heapq.heappop(fila)
        
        if (x, y) == fim_ponto:
            return custo, caminho
            
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < len(labirinto) and 0 <= ny < len(labirinto[0]):
                if labirinto[nx][ny] == ' ' and (nx, ny) not in visitados:
                    heapq.heappush(fila, (custo + 1, (nx, ny), caminho + [(nx, ny)]))
                    
    return float('inf'), []

pontos_importantes = [inicio] + alvos + [objetivo]
dados_rotas = {}

for i, p1 in enumerate(pontos_importantes):
    for j, p2 in enumerate(pontos_importantes):
        if i < j:
            d, cam = ucs_caminho_exato(lab, p1, p2)
            dados_rotas[(p1, p2)] = (d, cam)
            dados_rotas[(p2, p1)] = (d, cam[::-1])

def funcao_custo(ordem, pre_dados):
    custo = pre_dados[(inicio, ordem[0])][0]
    for i in range(len(ordem) - 1):
        custo += pre_dados[(ordem[i], ordem[i+1])][0]
    custo += pre_dados[(ordem[-1], objetivo)][0]
    return custo

def gerar_vizinho(ordem_atual):
    vizinho = ordem_atual[:]
    if len(ordem_atual) < 2:
        return vizinho
    i, j = random.sample(range(len(ordem_atual)), 2)
    if i > j:
        i, j = j, i
    if random.random() < 0.5:
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    else:
        vizinho[i:j+1] = reversed(vizinho[i:j+1])
    return vizinho

def hill_climbing(pre_dados, alvos):
    ordem_atual = list(alvos)
    random.shuffle(ordem_atual)
    custo_atual = funcao_custo(ordem_atual, pre_dados)
    
    historico_convergencia = []
    iteracoes = 0
    
    for _ in range(1000):
        iteracoes += 1
        vizinho = gerar_vizinho(ordem_atual)
        custo_vizinho = funcao_custo(vizinho, pre_dados)
        
        if custo_vizinho <= custo_atual:
            ordem_atual = vizinho
            custo_atual = custo_vizinho
            
        historico_convergencia.append(custo_atual)
            
    return ordem_atual, custo_atual, historico_convergencia, iteracoes

def simulated_annealing(pre_dados, alvos, temperatura=10000, resfriamento=0.95):
    ordem_atual = list(alvos)
    random.shuffle(ordem_atual)
    custo_atual = funcao_custo(ordem_atual, pre_dados)
    
    historico_convergencia = []
    iteracoes = 0
    
    while temperatura > 0.1:
        iteracoes += 1
        vizinho = gerar_vizinho(ordem_atual)
        custo_vizinho = funcao_custo(vizinho, pre_dados)
        delta = custo_vizinho - custo_atual
        
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            ordem_atual = vizinho
            custo_atual = custo_vizinho
            
        historico_convergencia.append(custo_atual)
        temperatura *= resfriamento
        
    return ordem_atual, custo_atual, historico_convergencia, iteracoes

# =====================================================================
# MÓDULO OBRIGATÓRIO DE MÉTRICAS E MÚLTIPLAS EXECUÇÕES
# =====================================================================
NUM_EXECUCOES = 30

def coletar_estatisticas(algoritmo_func, nome_algoritmo, pre_dados, alvos):
    custos = []
    tempos = []
    iteracoes_totais = []
    historicos_curvas = []
    melhor_ordem_global = list(alvos)
    melhor_custo_global = float('inf')
    
    for _ in range(NUM_EXECUCOES):
        t_inicio = time.time()
        ordem, custo, hist, iters = algoritmo_func(pre_dados, alvos)
        t_fim = time.time()
        
        custos.append(custo)
        tempos.append(t_fim - t_inicio)
        iteracoes_totais.append(iters)
        historicos_curvas.append(hist)
        
        if custo < melhor_custo_global:
            melhor_custo_global = custo
            melhor_ordem_global = ordem
            
    return custos, tempos, iteracoes_totais, historicos_curvas, melhor_ordem_global, melhor_custo_global

hc_custos, hc_tempos, hc_iters, hc_curvas, hc_melhor_ordem, hc_min = coletar_estatisticas(hill_climbing, "Hill Climbing", dados_rotas, alvos)
sa_custos, sa_tempos, sa_iters, sa_curvas, sa_melhor_ordem, sa_min = coletar_estatisticas(simulated_annealing, "Simulated Annealing", dados_rotas, alvos)

custo_otimo_global = min(hc_min, sa_min)

def calcular_e_exibir_metricas(custos, tempos, iters, nome):
    melhor = min(custos)
    pior = max(custos)
    medio_custo = np.mean(custos)
    medio_tempo = np.mean(tempos)
    medio_iters = np.mean(iters)
    
    sucessos = sum(1 for c in custos if c <= custo_otimo_global)
    taxa_sucesso = (sucessos / NUM_EXECUCOES) * 100 if custo_otimo_global != float('inf') else 0.0
    
    print(f"\n==========================================")
    print(f" RELATÓRIO DE MÉTRICAS: {nome.upper()}")
    print(f"==========================================")
    print(f"• Melhor custo encontrado: {melhor} passos")
    print(f"• Pior custo encontrado: {pior} passos")
    print(f"• Custo médio ({NUM_EXECUCOES} execuções): {medio_custo:.2f} passos")
    print(f"• Tempo médio de execução: {medio_tempo:.4f} segundos")
    print(f"• Número médio de iterações: {medio_iters:.1f}")
    print(f"• Taxa de sucesso (atingir melhor custo {custo_otimo_global}): {taxa_sucesso:.2f}%")

calcular_e_exibir_metricas(hc_custos, hc_tempos, hc_iters, "Hill Climbing")
calcular_e_exibir_metricas(sa_custos, sa_tempos, sa_iters, "Simulated Annealing")

# =====================================================================
# GRÁFICO OBRIGATÓRIO: CURVA DE CONVERGÊNCIA (Iteração x Melhor Custo)
# =====================================================================
plt.figure(figsize=(10, 6))

hc_comprimento_min = min(len(h) for h in hc_curvas)
hc_curva_media = np.mean([h[:hc_comprimento_min] for h in hc_curvas], axis=0)

sa_comprimento_min = min(len(h) for h in sa_curvas)
sa_curva_media = np.mean([h[:sa_comprimento_min] for h in sa_curvas], axis=0)

plt.plot(hc_curva_media, color='orangered', linewidth=2, label='Hill Climbing (Média)')
plt.plot(sa_curva_media, color='dodgerblue', linewidth=2, label='Simulated Annealing (Média)')

plt.title('Curva de Convergência: Iteração × Melhor Custo (Média de 30 Execuções)', fontsize=12, weight='bold')
plt.xlabel('Iteração', fontsize=11)
plt.ylabel('Melhor Custo Encontrado (Passos)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.show()

# =====================================================================
# 6. Plotagem Gráfica Dinâmica Passo a Passo (Para AMBOS os algoritmos)
# =====================================================================
def plotar_solucao_passo_a_passo(labirinto, ordem_solucao, dados_rotas, titulo, custo):
    h, w = len(labirinto), len(labirinto[0])
    matriz_lab = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            if labirinto[i][j] == '#':
                matriz_lab[i][j] = 1
                
    plt.figure(figsize=(11, 9))
    plt.imshow(matriz_lab, cmap='binary', origin='upper')
    
    nome_checkpoints = {v: k for k, v in checkpoints_dict.items()}
    cores_segmentos = ['#FF5733', '#33FF57', '#3357FF', '#900C3F'] 
    
    cadeia_pontos = [inicio] + ordem_solucao + [objetivo]
    nomes_cadeia = ['A'] + [nome_checkpoints[p] for p in ordem_solucao] + ['B']
    
    for idx in range(len(cadeia_pontos) - 1):
        p_atual = cadeia_pontos[idx]
        p_proximo = cadeia_pontos[idx+1]
        
        trecho_coordenadas = dados_rotas[(p_atual, p_proximo)][1]
        trecho_y = [p[0] for p in trecho_coordenadas]
        trecho_x = [p[1] for p in trecho_coordenadas]
        
        rotulo_trecho = f"Etapa {idx+1}: {nomes_cadeia[idx]} -> {nomes_cadeia[idx+1]}"
        plt.plot(trecho_x, trecho_y, color=cores_segmentos[idx], linewidth=4, label=rotulo_trecho, zorder=1)
    
    plt.scatter(posicoes_originais['A'][1], posicoes_originais['A'][0], color='cyan', s=250, marker='o', label='Partida (A)', zorder=2)
    plt.scatter(posicoes_originais['B'][1], posicoes_originais['B'][0], color='crimson', s=250, marker='X', label='Chegada (B)', zorder=2)
    
    for nome in checkpoints_dict.keys():
        pos = posicoes_originais[nome]
        plt.scatter(pos[1], pos[0], color='gold', s=180, marker='*', zorder=2)
        plt.text(pos[1] + 0.6, pos[0] - 0.6, nome, fontsize=12, weight='bold', color='darkorange', 
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

    sequencia_nomes = " -> ".join([nome_checkpoints[p] for p in ordem_solucao])
    plt.title(f"{titulo}\nFluxo OBRIGATÓRIO: A -> {sequencia_nomes} -> B\nPassos Totais Percorridos: {custo} Passos", fontsize=13, weight='bold')
    plt.legend(loc='upper right', framealpha=0.95)
    plt.axis('on')
    plt.show()

plotar_solucao_passo_a_passo(lab, hc_melhor_ordem, dados_rotas, "Caminho Sequencial - Hill Climbing", min(hc_custos))
plotar_solucao_passo_a_passo(lab, sa_melhor_ordem, dados_rotas, "Caminho Sequencial - Simulated Annealing", min(sa_custos))