# Busca Online no Labirinto Desconhecido

Trabalho Prático — Parte IV (Semana 3)  
Agente Inteligente em Labirinto — Busca Online

## Descrição

Implementação de um agente inteligente que navega em um labirinto desconhecido, construindo um mapa interno progressivamente. O agente utiliza o ciclo: **perceber → atualizar mapa → planejar → agir**.

## Algoritmos Implementados

1. **Replanning A*** — O agente planeja com A* no mapa parcial e replaneja quando encontra obstáculos
2. **Online DFS** — Exploração sistemática com backtracking

## Requisitos

```bash
pip install matplotlib pygame
```

## Execução

```bash
# Execução completa (experimentos + gráficos + visualização)
python main.py

# Sem visualização Pygame
python main.py --no-viz

# Apenas visualização
python main.py --viz-only --algo replanning
python main.py --viz-only --algo dfs
```

## Estrutura

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Ponto de entrada |
| `maze.py` | Representação do labirinto |
| `classical_search.py` | A* offline (referência) |
| `online_search.py` | Algoritmos de busca online |
| `metrics.py` | Coleta de métricas |
| `graphs.py` | Geração de gráficos |
| `visualization.py` | Visualização Pygame |
| `lab3.txt` | Labirinto |
| `relatorio_tecnico.md` | Relatório técnico |
| `relatorio_codigo.md` | Explicação do código |

## Resultados

- CSV: `results/resultados_experimentais.csv`
- Gráficos: `results/graphs/`

## Controles da Visualização

| Tecla | Ação |
|-------|------|
| SPACE | Pausar/Continuar |
| ← → | Passo anterior/próximo |
| ↑ ↓ | Velocidade +/- |
| HOME/END | Início/Fim |
| ESC | Sair |
