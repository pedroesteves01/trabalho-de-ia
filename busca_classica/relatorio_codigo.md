# Relatório de Código — Busca Clássica no Labirinto

## Estrutura do Projeto

```
busca_classica/
├── main.py              # Ponto de entrada, classe LabirintoProblema, visualização
├── buscaClassica.py     # Implementação dos 5 algoritmos de busca
└── lab1.txt             # Labirinto 17×25
```

---

## 1. `buscaClassica.py` — Algoritmos de Busca

### Estruturas de Dados

**Classe `No`** — Representa um nó na árvore de busca:

```python
class No:
    def __init__(self, estado, pai=None, acao=None, g=0.0):
        self.estado = estado   # (linha, coluna)
        self.pai = pai         # nó pai para reconstrução
        self.acao = acao       # ação que levou a este nó
        self.g = g             # custo acumulado do início até aqui
```

O método `__lt__` garante desempate na fila de prioridade pelo custo `g`.

**`ResultadoBusca`** — NamedTuple padronizada com todas as métricas obrigatórias:

```python
class ResultadoBusca(NamedTuple):
    algoritmo: str
    sucesso: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    max_fronteira: int
    tempo_execucao: float
```

### Função `busca_largura()` (BFS)

Implementa busca em largura usando `deque` como fila FIFO.

**Estruturas de controle:**
- `fronteira`: fila de nós a expandir
- `em_fronteira`: conjunto para verificação rápida de pertencimento
- `explorados`: conjunto de estados já visitados

**Fluxo:**
1. Retira nó da frente da fila (`popleft`)
2. Testa se é objetivo
3. Adiciona a explorados e gera filhos
4. Filhos que não estão em explorados nem na fronteira são enfileirados

### Função `busca_profundidade()` (DFS)

Idêntica ao BFS, mas usa a lista como pilha LIFO (`pop` em vez de `popleft`). Isso faz com que os últimos nós adicionados sejam expandidos primeiro, criando exploração em profundidade.

### Função `busca_prioridade()` (Genérica)

Função unificada para UCS, Gulosa e A*. Recebe uma `funcao_prioridade` como parâmetro que determina o comportamento:

```python
def busca_prioridade(self, nome, funcao_prioridade):
```

**Estruturas de controle:**
- `fronteira`: heap de prioridade (`heapq`) com tuplas `(prioridade, contador, nó)`
- `melhor_g`: dicionário de melhor custo conhecido por estado (evita reexpansões desnecessárias)
- `fechados`: conjunto de estados já expandidos
- `contador`: desempatador via `itertools.count()` — evita comparação direta entre objetos `No`

**Fluxo:**
1. Retira nó com menor prioridade do heap
2. Se já está em `fechados`, ignora (poda)
3. Testa se é objetivo
4. Adiciona a fechados e gera filhos
5. Filhos com custo melhor que o registrado em `melhor_g` são inseridos no heap

### Funções Derivadas

Cada algoritmo chama `busca_prioridade` com uma lambda diferente:

| Algoritmo | Função de Prioridade |
|-----------|---------------------|
| UCS | `lambda no: no.g` |
| Gulosa | `lambda no: self.h(no.estado)` |
| A* | `lambda no: no.g + 1.0 * self.h(no.estado)` |
---

## 2. `main.py` — Classe Principal e Visualização

### Classe `LabirintoProblema`

Representa o problema de busca no labirinto:

```python
class LabirintoProblema:
    def __init__(self, grid):
        self.grid = grid
        self.inicio = self._encontrar_sinal('A')
        self.objetivo = self._encontrar_sinal('B')
```

**Método `vizinhos(estado)`:**
Retorna os vizinhos válidos de uma posição — movimentos ortogonais (cima, baixo, esquerda, direita) que estejam dentro dos limites e não sejam paredes.

```python
def vizinhos(self, estado):
    # Retorna lista de (ação, novo_estado, custo)
    # Custo fixo de 1.0 por movimento
```

**Método `h(estado)`:**
Heurística de Manhattan — distância mínima em grade sem obstáculos:

$$h(n) = |x_n - x_{objetivo}| + |y_n - y_{objetivo}|$$

**Método `reconstruir(no)`:**
Reconstrói o caminho seguindo ponteiros `pai` do nó objetivo até a raiz.

### Função `ler_labirinto(caminho_arquivo)`

Carrega o arquivo `.txt` e converte cada linha em uma lista de caracteres. Valida extensão e existência do arquivo.

### Visualização com Matplotlib

**`exibir_mapa_original_matplotlib()`:**
Renderiza o labirinto como uma imagem matricial usando `imshow`:
- Preto (`#1A1A1A`): paredes
- Branco: células livres
- Verde (`#2ECC71`): posição inicial (A)
- Vermelho (`#E74C3C`): objetivo (B)

**`exibir_resultado_matplotlib()`:**
Mostra o labirinto com o caminho encontrado destacado em azul (`#3498DB`). Salva a imagem como PNG (`resultado_<algoritmo>.png`).

**`exibir_grafico_desempenho_individual()`:**
Gera gráfico de barras com 4 métricas (Custo, Expandidos, Explorados, Fronteira) e uma caixa lateral com o "Raio-X do Agente" contendo algoritmo, tempo e utilidade J.

### Fluxo de Execução (`main()`)

1. Solicita caminho do arquivo do labirinto via `input()`
2. Exibe mapa original com Matplotlib
3. Lista funções de busca disponíveis em `buscaClassica.py` usando `inspect.getmembers()`
4. Usuário escolhe qual algoritmo executar
5. Executa a busca e calcula a utilidade J
6. Exibe tabela de resultados no terminal
7. Plota a solução no labirinto e o gráfico de desempenho

**Cálculo da Utilidade:**

$$J = -(0.15 \times \text{custo} + 0.15 \times \text{nós expandidos})$$

**Descoberta dinâmica de funções:**
O código usa `inspect.getmembers(buscaClassica, inspect.isfunction)` para listar automaticamente todas as funções de busca disponíveis, filtrando pelo prefixo `busca_` e excluindo `busca_prioridade` (função auxiliar interna).
