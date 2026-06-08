# Agente Inteligente em Labirinto — Trabalho Prático

Trabalho Prático de Inteligência Artificial  
Agente Inteligente para navegação em labirintos com três abordagens de busca.

## Requisitos

```bash
pip install matplotlib pygame numpy
```

---

## 1. Busca Clássica (Parte II — Semana 1)

Implementação de 5 algoritmos de busca clássica com mapa completo: **BFS, DFS, UCS, Busca Gulosa e A***.

**Labirinto:** `busca_classica/lab1.txt` (17×25)

### Execução

```bash
cd busca_classica
python main.py
```

O programa solicita o caminho do arquivo do labirinto e o algoritmo a executar. Para executar com o labirinto padrão, informe `lab1.txt`.

### Relatórios

- [Relatório Técnico](busca_classica/relatorio_tecnico.md)
- [Relatório de Código](busca_classica/relatorio_codigo.md)

---

## 2. Busca Local (Parte III — Semana 2)

Otimização de rotas com **Hill Climbing** e **Simulated Annealing** para visitar pontos de coleta (C1, C2, C3) no menor percurso possível.

**Labirinto:** `busca_local/lab2.txt` (19×33 com checkpoints)

### Execução

```bash
cd busca_local
python algoritmo.py
```

Executa automaticamente 30 rodadas de cada algoritmo, exibe métricas no terminal e gera gráficos de convergência e solução.

### Relatórios

- [Relatório Técnico](busca_local/relatorio_tecnico.md)
- [Relatório de Código](busca_local/relatorio_codigo.md)

---

## 3. Busca Online (Parte IV — Semana 3)

Agente que navega em labirinto **desconhecido**, construindo mapa interno progressivamente. Implementa **Replanning A*** e **Online DFS**.

**Labirinto:** `lab3.txt` (17×25 com regiões desconhecidas `?`)

### Execução

```bash
# Execução completa (experimentos + gráficos + visualização Pygame)
python main.py

# Sem visualização Pygame
python main.py --no-viz

# Apenas visualização interativa
python main.py --viz-only --algo replanning
python main.py --viz-only --algo dfs
```

### Relatórios

- [Relatório Técnico](relatorio_tecnico.md)
- [Relatório de Código](relatorio_codigo.md)

---

## Estrutura do Projeto

```
ai/
├── README.md                          # Este arquivo
├── busca_classica/
│   ├── main.py                        # Entrada principal e visualização
│   ├── buscaClassica.py               # 5 algoritmos de busca
│   ├── lab1.txt                       # Labirinto
│   ├── relatorio_tecnico.md           # Relatório técnico
│   └── relatorio_codigo.md            # Relatório de código
├── busca_local/
│   ├── algoritmo.py                   # Hill Climbing + Simulated Annealing
│   ├── lab2.txt                       # Labirinto com checkpoints
│   ├── relatorio_tecnico.md           # Relatório técnico
│   └── relatorio_codigo.md            # Relatório de código
├── main.py                            # Entrada da busca online
├── maze.py                            # Representação do labirinto
├── classical_search.py                # A* offline (referência)
├── online_search.py                   # Algoritmos de busca online
├── metrics.py                         # Coleta de métricas
├── graphs.py                          # Geração de gráficos
├── visualization.py                   # Visualização Pygame
├── lab3.txt                           # Labirinto com regiões desconhecidas
├── relatorio_tecnico.md               # Relatório técnico (busca online)
└── relatorio_codigo.md                # Relatório de código (busca online)
```
