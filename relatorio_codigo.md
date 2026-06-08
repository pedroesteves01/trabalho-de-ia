# Relatório de Código — Explicação Detalhada

## Estrutura do Projeto

```
ai/
├── main.py                 # Ponto de entrada principal
├── maze.py                 # Representação do labirinto (real + interno)
├── classical_search.py     # A* offline (referência)
├── online_search.py        # Algoritmos de busca online
├── metrics.py              # Coleta e exportação de métricas
├── graphs.py               # Geração de gráficos de desempenho
├── visualization.py        # Visualização interativa com Pygame
├── lab3.txt                # Arquivo do labirinto
├── relatorio_tecnico.md    # Relatório técnico
├── relatorio_codigo.md     # Este arquivo
└── results/
    ├── resultados_experimentais.csv
    └── graphs/
        ├── razao_online_offline.png
        ├── movimentos_totais.png
        ├── reveladas_vs_revisitadas.png
        ├── replanejamentos.png
        ├── tempo_execucao.png
        ├── comparacao_geral.png
        └── progressao_descoberta.png
```

---

## 1. `maze.py` — Representação do Labirinto

### Classe `Maze` (Mapa Real)

Esta classe carrega e representa o **mapa real** do labirinto, usado pelo simulador.

**Decisões de design:**
- O arquivo `lab3.txt` contém `?` para representar células livres no modo online. Na carga do mapa real, `?` é convertido para espaço (célula livre), pois o simulador conhece a verdade.
- `A` e `B` são registrados como posições especiais, mas suas células são tratadas como livres no grid.
- O método `get_neighbors()` retorna vizinhos válidos (livres e dentro dos limites) nas 4 direções ortogonais.

```python
def _load(self, filepath):
    # '?' → célula livre (o mapa real sabe o que é)
    # 'A' → registra start, célula livre
    # 'B' → registra goal, célula livre
    # '#' → parede
```

### Classe `AgentMap` (Mapa Interno)

Representa o que o agente **sabe** sobre o labirinto. Começa completamente preenchido com `?` (desconhecido), exceto a posição inicial.

**Decisões de design:**
- `get_passable_neighbors()` retorna vizinhos que **não são paredes conhecidas** — inclui tanto células livres quanto desconhecidas. Isso é fundamental para o planejamento otimista no A*.
- `get_known_neighbors()` retorna apenas vizinhos **confirmadamente livres** — usado quando se quer certeza.
- A separação entre mapa real e mapa do agente impõe a restrição de que o agente nunca "trapaceia".

---

## 2. `classical_search.py` — A* Offline

### Função `astar_offline(maze, start, goal)`

Implementação padrão do A* no mapa completo. Serve como **baseline** para calcular o custo ótimo.

**Componentes:**
- **Open set:** Min-heap (heapq) ordenado por f(n) = g(n) + h(n)
- **g_score:** Custo real do início até cada nó
- **f_score:** Estimativa de custo total via cada nó
- **came_from:** Mapa de predecessores para reconstrução do caminho

**Heurística:** Manhattan distance — admissível e consistente para movimentos em grade.

### Função `astar_on_partial_map(agent_map, start, goal)`

A* executado no **mapa parcial** do agente. A diferença crucial é que usa `get_passable_neighbors()`, tratando células desconhecidas como potencialmente livres.

**Por que heurística otimista?**
- Se tratássemos `?` como paredes, o agente não encontraria caminho até explorar o suficiente.
- Ao assumir `?` como livre, o agente planeja o melhor caminho possível e descobre bloqueios durante a execução.
- Esta é a abordagem padrão em busca online com replanning.

---

## 3. `online_search.py` — Algoritmos de Busca Online

### Classe Base `OnlineAgent`

Encapsula a lógica comum a todos os agentes online:

```python
def _perceive(self):
    # Revela células no raio r usando distância de Manhattan
    # Atualiza mapa interno com FREE ou WALL

def _move_to(self, next_pos):
    # Move o agente, incrementa métricas, percebe novo entorno

def _save_state(self):
    # Salva snapshot para visualização
```

**Percepção (raio r):**
O agente percebe todas as células $(nr, nc)$ tais que $|dr| + |dc| \leq r$. Isso cria um padrão em losango (Manhattan ball) ao redor do agente.

### `ReplanningAStarAgent` (Opção A)

**Algoritmo:**
```
ENQUANTO não chegou ao objetivo:
    1. Executa A* no mapa parcial (current_pos → goal)
    2. Para cada passo no caminho planejado:
       a. Se o passo é livre no mapa REAL → move
       b. Se o passo é parede → atualiza mapa, REPLANEJA
```

**Decisões chave:**
- O agente tenta seguir o caminho planejado **inteiro** até encontrar um obstáculo. Isso é mais eficiente que replanejar a cada passo.
- Quando encontra uma parede inesperada, marca no mapa interno e volta ao loop externo para replanejar.
- Limite de segurança (`max_steps`) previne loops infinitos em labirintos sem solução.

### `OnlineDFSAgent` (Opção B)

**Algoritmo:**
```
ENQUANTO não chegou ao objetivo:
    1. Inicializa vizinhos não visitados para posição atual
    2. Se há vizinhos não visitados:
       → Move para o primeiro não visitado
    3. Senão:
       → Backtrack (volta pelo caminho registrado)
```

**Estruturas de dados:**
- `visited`: Set de posições já visitadas
- `untried`: Dict {pos → [vizinhos não testados]}
- `unbacktracked`: Dict {pos → [posições de retorno]}

**Por que DFS é subótimo?**
- Não possui heurística — explora em ordem fixa (cima, baixo, esquerda, direita)
- Backtracking gera muitas revisitas
- Pode explorar becos profundos antes de tentar direções promissoras

---

## 4. `metrics.py` — Coleta de Métricas

### `run_experiment(maze_path, perception_radius)`

Orquestra uma execução completa:
1. Calcula caminho ótimo offline (referência)
2. Executa Replanning A*
3. Executa Online DFS
4. Calcula razão online/offline para cada

### `run_multiple_radius_experiments(maze_path, radii)`

Executa experimentos com raios [1, 2, 3] para análise comparativa do impacto da percepção.

### `save_results_csv(results, output_path)`

Exporta resultados em formato CSV para análise externa.

---

## 5. `graphs.py` — Geração de Gráficos

Gera 7 gráficos usando Matplotlib:

| Gráfico | O que mostra |
|---------|-------------|
| `razao_online_offline.png` | Barras comparando eficiência relativa |
| `movimentos_totais.png` | Linhas mostrando custo por raio |
| `reveladas_vs_revisitadas.png` | Eficiência de exploração |
| `replanejamentos.png` | Overhead computacional |
| `tempo_execucao.png` | Performance temporal |
| `comparacao_geral.png` | Visão consolidada |
| `progressao_descoberta.png` | Curva de aprendizado do mapa |

**Decisão:** Uso do backend `Agg` (não-interativo) para gerar imagens sem necessidade de display.

---

## 6. `visualization.py` — Visualização Interativa

### `visualize_online_search()`

Visualização step-by-step com Pygame mostrando:
- **Amarelo:** Posição atual do agente
- **Vermelho:** Objetivo (B)
- **Branco:** Células livres conhecidas
- **Cinza escuro:** Paredes descobertas
- **Azul escuro (FOG):** Células desconhecidas
- **Ciano:** Caminho percorrido pelo agente
- **Verde claro:** Caminho ótimo offline (referência)

**Controles interativos:**
- `SPACE`: Pausar/Continuar animação
- `← →`: Navegar passo a passo
- `↑ ↓`: Controlar velocidade
- `HOME/END`: Ir ao início/fim
- `ESC`: Sair

**Decisão de design:** A visualização mostra simultaneamente o que o agente sabe (mapa interno) e seu progresso, permitindo observar como a "névoa de guerra" se dissipa conforme ele explora.

---

## 7. `main.py` — Ponto de Entrada

Orquestra todo o pipeline:

```
1. Carrega labirinto
2. Executa experimentos (raios 1, 2, 3)
3. Imprime resultados formatados no terminal
4. Salva CSV
5. Gera gráficos
6. Inicia visualização Pygame (se disponível)
```

**Flags de linha de comando:**
- `--no-viz`: Desabilita visualização (útil para CI/automação)
- `--viz-only`: Apenas visualização (pula geração de gráficos completa)
- `--algo replanning|dfs`: Filtra qual algoritmo visualizar

---

## Decisões Arquiteturais

### 1. Separação Real vs. Interno
A principal decisão foi manter uma separação rígida entre o **mapa real** (classe `Maze`) e o **mapa do agente** (classe `AgentMap`). O agente nunca acessa `Maze` diretamente — ele só recebe percepções através do método `_perceive()`. Isso garante a integridade da simulação.

### 2. Heurística Otimista
No A* parcial, células desconhecidas são tratadas como **potencialmente livres**. Alternativa seria tratá-las como paredes (pessimista), mas isso impediria o planejamento até o mapa estar quase todo revelado.

### 3. Seguir Caminho vs. Passo Único
O Replanning A* segue o caminho planejado até encontrar um obstáculo, ao invés de replanejar a cada passo. Isso é mais eficiente (menos execuções de A*) e ainda garante corretude porque verificamos cada passo contra o mapa real.

### 4. Percepção Manhattan Ball
A percepção usa distância de Manhattan (losango) ao invés de Chebyshev (quadrado). Isso é consistente com o modelo de movimentos ortogonais e é a escolha padrão na literatura.

### 5. Métricas Progressivas
O `OnlineSearchMetrics` registra snapshots do mapa a cada passo para possibilitar visualização posterior. O custo de memória é aceitável para labirintos do tamanho usado.

---

## Como Executar

```bash
# Instalar dependências
pip install matplotlib pygame

# Execução completa (experimentos + gráficos + visualização)
python main.py

# Apenas experimentos e gráficos (sem janela Pygame)
python main.py --no-viz

# Apenas visualização do Replanning A*
python main.py --viz-only --algo replanning

# Apenas visualização do Online DFS
python main.py --viz-only --algo dfs
```

---

## Complexidade

| Algoritmo | Tempo (pior caso) | Espaço |
|-----------|-------------------|--------|
| A* Offline | $O(b^d)$ | $O(b^d)$ |
| Replanning A* | $O(k \cdot b^d)$ onde k = replanejamentos | $O(n)$ onde n = células |
| Online DFS | $O(n^2)$ com backtracking | $O(n)$ |

Para o labirinto 17×25 (425 células), todos os algoritmos executam em milissegundos.
