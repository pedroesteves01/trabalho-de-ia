# Relatório de Código — Busca Local no Labirinto com Pontos de Coleta

## Estrutura do Projeto

```
busca_local/
├── algoritmo.py     # Implementação completa (leitura, algoritmos, métricas, gráficos)
└── lab2.txt         # Labirinto 19×33 com checkpoints C1, C2, C3
```

---

## 1. Leitura e Processamento do Labirinto

### Função `ler_labirinto_e_limpar(nome_arquivo)`

Carrega o labirinto e resolve o problema de **checkpoints multi-caractere** (e.g., "C1" ocupa 2 colunas no arquivo texto).

**Etapas:**
1. Lê o arquivo e normaliza linhas (padding com `#` até a largura máxima)
2. Detecta checkpoints dinamicamente: procura padrões `C` seguido de dígito
3. Converte posições dos checkpoints e marcadores (A, B) em espaços livres
4. Aplica `garantir_ponto_livre()` para ajustar pontos que caiam em paredes

```python
# Detecção dinâmica de checkpoints
for i in range(len(labirinto)):
    for j in range(len(labirinto[i]) - 1):
        if labirinto[i][j] == 'C' and labirinto[i][j+1].isdigit():
            nome_cp = 'C' + labirinto[i][j+1]
            checkpoints_brutos[nome_cp] = (i, j)
```

**Função `garantir_ponto_livre()`:**
Se um ponto de interesse cai sobre uma parede após a limpeza, busca o vizinho livre mais próximo nas 4 direções ortogonais. Isso trata casos de borda onde o caractere multi-coluna pode gerar colisão com paredes.

---

## 2. Pré-computação de Rotas — UCS

### Função `ucs_caminho_exato(labirinto, inicio, fim)`

Implementa a **Busca de Custo Uniforme** para encontrar o menor caminho real entre dois pontos no labirinto, retornando tanto o custo quanto a lista de coordenadas do caminho.

```python
def ucs_caminho_exato(labirinto, inicio_ponto, fim_ponto):
    fila = [(0, inicio_ponto, [inicio_ponto])]  # (custo, posição, caminho)
    visitados = set()
    # ...heapq para expandir por menor custo...
    return custo, caminho
```

**Pré-computação:**
Calcula rotas entre **todos os pares** de pontos importantes:

```python
pontos_importantes = [inicio] + alvos + [objetivo]  # A, C1, C2, C3, B
for i, p1 in enumerate(pontos_importantes):
    for j, p2 in enumerate(pontos_importantes):
        if i < j:
            dados_rotas[(p1, p2)] = ucs(p1, p2)
            dados_rotas[(p2, p1)] = (custo, caminho_reverso)
```

Com 5 pontos, calcula $\binom{5}{2} = 10$ rotas. Cada rota é armazenada em ambas as direções no dicionário `dados_rotas`.

---

## 3. Função de Custo

### Função `funcao_custo(ordem, pre_dados)`

Avalia o custo total de uma permutação usando as rotas pré-computadas:

$$f(\pi) = d(A, \pi_1) + \sum_{i=1}^{k-1} d(\pi_i, \pi_{i+1}) + d(\pi_k, B)$$

```python
def funcao_custo(ordem, pre_dados):
    custo = pre_dados[(inicio, ordem[0])][0]           # A → primeiro checkpoint
    for i in range(len(ordem) - 1):
        custo += pre_dados[(ordem[i], ordem[i+1])][0]  # entre checkpoints
    custo += pre_dados[(ordem[-1], objetivo)][0]        # último → B
    return custo
```

---

## 4. Função de Vizinhança

### Função `gerar_vizinho(ordem_atual)`

Gera uma solução vizinha por uma de duas operações (50% de probabilidade cada):

- **Swap:** seleciona dois índices aleatórios e troca seus valores
- **2-opt (Reversão):** seleciona dois índices e inverte o segmento entre eles

```python
if random.random() < 0.5:
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]  # swap
else:
    vizinho[i:j+1] = reversed(vizinho[i:j+1])        # 2-opt
```

---

## 5. Algoritmos de Busca Local

### Função `hill_climbing(pre_dados, alvos)`

- Inicia com permutação aleatória dos checkpoints
- Executa 1000 iterações, aceitando apenas vizinhos com $f \leq f_{\text{atual}}$
- Registra histórico de convergência para plotagem

### Função `simulated_annealing(pre_dados, alvos, temperatura, resfriamento)`

- Inicia com permutação aleatória
- Aceita vizinhos piores com probabilidade $P = e^{-\Delta / T}$
- Temperatura reduz geometricamente: $T \leftarrow 0.95 \times T$
- Termina quando $T < 0.1$ (resulta em ~225 iterações)

---

## 6. Módulo de Métricas

### Função `coletar_estatisticas(algoritmo_func, nome, pre_dados, alvos)`

Executa o algoritmo **30 vezes** e coleta:
- Custos de cada execução
- Tempos de execução
- Número de iterações
- Históricos de convergência (para curva média)
- Melhor solução global encontrada

### Função `calcular_e_exibir_metricas(custos, tempos, iters, nome)`

Calcula e exibe no terminal:
- Melhor/pior/médio custo
- Tempo médio
- Iterações médias
- Taxa de sucesso (% de execuções que atingiram o melhor custo global)

---

## 7. Visualizações

### Curva de Convergência

Gráfico de **Iteração × Melhor Custo** com curvas médias (30 execuções) para ambos os algoritmos. Trunca ao comprimento da menor execução para calcular a média corretamente.

```python
hc_curva_media = np.mean([h[:comprimento_min] for h in hc_curvas], axis=0)
```

### Função `plotar_solucao_passo_a_passo()`

Renderiza o labirinto com o caminho completo da melhor solução, mostrando:
- **Segmentos coloridos:** cada trecho (A→C_i, C_i→C_j, C_k→B) com cor distinta
- **Marcadores:** A (ciano), B (vermelho), checkpoints (estrelas douradas)
- **Título:** inclui o fluxo obrigatório e o custo total em passos

```python
cores_segmentos = ['#FF5733', '#33FF57', '#3357FF', '#900C3F']
```

Usa as coordenadas reais dos caminhos pré-computados (via `dados_rotas`) para traçar os segmentos sobre o mapa do labirinto renderizado com `imshow`.
