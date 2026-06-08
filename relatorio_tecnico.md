# Relatório Técnico — Busca Online no Labirinto Desconhecido

## Trabalho Prático — Parte IV (Semana 3)
**Curso:** Engenharia de Computação / Sistemas de Informação  
**Linguagem:** Python  
**Tema:** Agente Inteligente com Busca Online

---

## 1. Introdução

Este relatório apresenta a implementação e análise da **Parte IV** do trabalho prático: a **Busca Online no Labirinto Desconhecido**. Nesta etapa, o agente não possui acesso ao mapa completo do labirinto e deve explorá-lo progressivamente enquanto se move em direção ao objetivo.

O desafio central é que, diferentemente da busca clássica (onde o agente planeja com o mapa completo), na busca online o agente deve **descobrir o mapa enquanto age**, seguindo o ciclo:

$$\text{perceber} \rightarrow \text{atualizar mapa interno} \rightarrow \text{planejar} \rightarrow \text{agir}$$

Foram implementadas duas estratégias:
- **Opção A:** Replanning com A*
- **Opção B:** Online DFS

---

## 2. Modelagem PEAS (Contexto Busca Online)

### Performance
A medida de desempenho para a busca online é:

$$J = -\alpha \cdot \text{custo percorrido} - \beta \cdot \text{células revisitadas} - \gamma \cdot \text{replanejamentos}$$

A métrica central é a **razão online/offline**:

$$\text{razão} = \frac{\text{custo percorrido pelo agente online}}{\text{custo ótimo no mapa completo}}$$

### Environment
- Labirinto 17×25 em grade discreta
- Células livres, paredes, posição inicial (A) e objetivo (B)
- **Regiões desconhecidas** (?) — o agente só percebe vizinhança local

### Actuators
$$A = \{\text{cima, baixo, esquerda, direita}\}$$

### Sensors
O agente percebe apenas uma vizinhança local com raio $r$:
- $r = 1$: percebe os 4 vizinhos ortogonais
- $r = 2$: percebe até 12 células adjacentes
- $r = 3$: percebe até 24 células próximas

---

## 3. Formulação Formal do Problema

O problema de busca online é formulado como:

$$\langle S, A, T, s_0, G, c, P \rangle$$

Onde:
- $S$: conjunto de posições do labirinto (parcialmente conhecidas)
- $A$: {cima, baixo, esquerda, direita}
- $T$: função de transição (determinística, mas parcialmente observável)
- $s_0$: posição inicial $A = (1, 1)$
- $G$: alcançar $B = (15, 20)$
- $c$: custo unitário por movimento
- $P$: função de percepção (raio $r$)

**Diferença da busca clássica:** O agente não conhece $T$ completamente. Ele descobre os resultados das ações apenas após executá-las ou percebê-las.

---

## 4. Descrição dos Algoritmos

### 4.1 Replanning com A* (Opção A)

O agente mantém um **mapa interno** progressivamente atualizado. A cada passo:

1. **Percebe** células na vizinhança (raio $r$)
2. **Atualiza** o mapa interno com as percepções
3. **Planeja** executando A* no mapa parcial (células desconhecidas são tratadas como potencialmente livres — heurística otimista)
4. **Age** executando o próximo passo do plano
5. Se encontra uma parede inesperada, **replaneja**

**Heurística:** Distância de Manhattan $h(n) = |x_n - x_B| + |y_n - y_B|$

### 4.2 Online DFS (Opção B)

O agente explora sistematicamente mantendo:
- **Estados visitados:** conjunto de posições já visitadas
- **Ações não testadas:** vizinhos não visitados de cada posição
- **Caminho de retorno:** pilha para backtracking

Quando não há vizinhos livres não visitados, o agente retorna pelo caminho de retorno (backtracking).

---

## 5. Metodologia Experimental

### Configuração
- **Labirinto:** `lab3.txt` (17×25, labirinto com corredores)
- **Raios de percepção testados:** $r \in \{1, 2, 3\}$
- **Referência:** Caminho ótimo offline calculado com A* completo

### Métricas Coletadas
| Métrica | Descrição |
|---------|-----------|
| Sucesso | O agente alcançou B? |
| Movimentos totais | Número de ações executadas |
| Custo real | Custo total do caminho percorrido |
| Células reveladas | Número de células descobertas |
| Células revisitadas | Número de visitas repetidas |
| Replanejamentos | Quantas vezes o agente replanejou |
| Razão online/offline | Custo online / custo ótimo |

---

## 6. Resultados

### 6.1 Caminho Ótimo Offline
| Métrica | Valor |
|---------|-------|
| Custo | 33 |
| Tamanho do caminho | 34 |
| Nós expandidos | 41 |

### 6.2 Replanning A*

| Raio | Sucesso | Custo Real | Revisitadas | Replanejamentos | Razão Online/Offline |
|------|---------|------------|-------------|-----------------|---------------------|
| 1 | Sim | 35 | 1 | 14 | 1.0606 |
| 2 | Sim | 35 | 1 | 8 | 1.0606 |
| 3 | Sim | 35 | 1 | 7 | 1.0606 |

### 6.3 Online DFS

| Raio | Sucesso | Custo Real | Revisitadas | Replanejamentos | Razão Online/Offline |
|------|---------|------------|-------------|-----------------|---------------------|
| 1 | Sim | 297 | 116 | 297 | 9.0000 |
| 2 | Sim | 297 | 116 | 297 | 9.0000 |
| 3 | Sim | 297 | 116 | 297 | 9.0000 |

---

## 7. Gráficos

Os gráficos gerados encontram-se na pasta `results/graphs/`:

1. **razao_online_offline.png** — Razão online/offline por raio de percepção
2. **movimentos_totais.png** — Movimentos totais por algoritmo
3. **reveladas_vs_revisitadas.png** — Células reveladas vs revisitadas
4. **replanejamentos.png** — Número de replanejamentos
5. **tempo_execucao.png** — Tempo de execução
6. **comparacao_geral.png** — Comparação geral entre algoritmos
7. **progressao_descoberta.png** — Progressão da descoberta do mapa

---

## 8. Limitações

1. **Heurística otimista no A* parcial:** Tratar células desconhecidas como livres pode levar a caminhos que se revelam bloqueados.
2. **Custo computacional:** Replanejamento frequente com A* pode ser custoso em labirintos muito grandes.
3. **DFS sem heurística:** O Online DFS não utiliza informação de direção, resultando em exploração ineficiente.
4. **Raio de percepção fixo:** Em cenários reais, a percepção pode variar com obstáculos.

---

## 9. Conclusão

A implementação demonstrou que:

1. **Replanning A*** é altamente eficiente para busca online, alcançando razão de apenas 1.06 em relação ao ótimo offline. A heurística de Manhattan e o planejamento otimista permitem ao agente encontrar caminhos quase ótimos mesmo sem conhecimento completo.

2. **Online DFS** garante encontrar o objetivo (completude), mas com custo muito superior (razão 9.0). É adequado como fallback em ambientes onde A* falha.

3. O **raio de percepção** tem impacto significativo no número de replanejamentos (14→7 com raio 1→3), mas pouco impacto no custo final para este labirinto.

4. A diferença fundamental entre busca online e clássica está no **trade-off entre informação e ação**: o agente online paga um "custo de exploração" por não conhecer o ambiente.
