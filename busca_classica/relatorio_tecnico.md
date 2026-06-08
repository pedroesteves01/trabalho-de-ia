# Relatório Técnico — Busca Clássica no Labirinto

## Trabalho Prático — Parte II (Semana 1)
**Curso:** Engenharia de Computação / Sistemas de Informação  
**Linguagem:** Python  
**Tema:** Algoritmos de Busca Clássica em Labirintos

---

## 1. Introdução

Este relatório apresenta a implementação e análise da **Parte II** do trabalho prático: a **Busca Clássica no Labirinto**. Nesta etapa, o agente possui acesso **completo** ao mapa do labirinto e deve encontrar o caminho do ponto inicial (A) até o objetivo (B) utilizando diferentes algoritmos de busca.

Foram implementados cinco algoritmos:
- **BFS** (Busca em Largura)
- **DFS** (Busca em Profundidade)
- **UCS** (Busca de Custo Uniforme)
- **Busca Gulosa** (Greedy Best-First)
- **A*** (A-Estrela)

---

## 2. Modelagem PEAS

### Performance
A medida de desempenho para a busca clássica é a **utilidade J**:

$$J = -(\alpha \cdot \text{custo do caminho} + \beta \cdot \text{nós expandidos})$$

Com $\alpha = 0.15$ e $\beta = 0.15$. Quanto maior J (menos negativo), melhor o desempenho.

### Environment
- Labirinto 17×25 em grade discreta (`lab1.txt`)
- Células livres (espaço), paredes (`#`), posição inicial (`A`) e objetivo (`B`)
- **Completamente observável** — o agente conhece todo o mapa antes de agir
- **Determinístico** — ações têm resultado previsível
- **Estático** — o ambiente não muda durante a execução

### Actuators
$$A = \{\text{cima, baixo, esquerda, direita}\}$$

### Sensors
O agente possui percepção **global** — tem acesso a toda a grade do labirinto, incluindo a posição de todas as paredes e células livres.

---

## 3. Formulação Formal do Problema

O problema de busca clássica é formulado como:

$$\langle S, A, T, s_0, G, c \rangle$$

Onde:
- $S$: conjunto de todas as posições $(r, c)$ livres no labirinto
- $A$: {cima, baixo, esquerda, direita}
- $T$: função de transição determinística e completamente conhecida
- $s_0$: posição inicial $A = (1, 1)$
- $G$: alcançar $B = (15, 22)$
- $c$: custo unitário por movimento ($c = 1.0$)

---

## 4. Descrição dos Algoritmos

### 4.1 BFS (Busca em Largura)

Explora o grafo nível a nível usando uma **fila FIFO**. Garante encontrar o caminho com menor número de passos (ótimo para custo unitário).

- **Fronteira:** `deque` (fila dupla)
- **Completude:** Sim
- **Otimalidade:** Sim (custo unitário)
- **Complexidade:** $O(b^d)$

### 4.2 DFS (Busca em Profundidade)

Explora o grafo em profundidade usando uma **pilha LIFO**. Não garante caminho ótimo.

- **Fronteira:** lista (pilha)
- **Completude:** Sim (com verificação de estados visitados)
- **Otimalidade:** Não
- **Complexidade:** $O(b^m)$

### 4.3 UCS (Busca de Custo Uniforme)

Expande o nó com menor custo acumulado $g(n)$. Equivalente ao BFS quando custos são unitários.

- **Fronteira:** heap de prioridade (por $g(n)$)
- **Completude:** Sim
- **Otimalidade:** Sim
- **Complexidade:** $O(b^{1+\lfloor C^*/\epsilon \rfloor})$

### 4.4 Busca Gulosa (Greedy Best-First)

Expande o nó com menor heurística $h(n)$. Rápida mas não garante caminho ótimo.

- **Fronteira:** heap de prioridade (por $h(n)$)
- **Heurística:** Distância de Manhattan $h(n) = |x_n - x_B| + |y_n - y_B|$
- **Completude:** Sim (com lista de fechados)
- **Otimalidade:** Não

### 4.5 A* (A-Estrela)

Combina custo real e heurística: $f(n) = g(n) + h(n)$. Encontra o caminho ótimo com a heurística admissível de Manhattan.

- **Fronteira:** heap de prioridade (por $f(n)$)
- **Heurística:** Distância de Manhattan (admissível e consistente)
- **Completude:** Sim
- **Otimalidade:** Sim
- **Complexidade:** $O(b^d)$ no caso típico

---

## 5. Metodologia Experimental

### Configuração
- **Labirinto:** `lab1.txt` (17×25 com corredores)
- **Posição inicial:** $A = (1, 1)$
- **Posição objetivo:** $B = (15, 22)$

### Métricas Coletadas
| Métrica | Descrição |
|---------|-----------|
| Sucesso | O algoritmo encontrou o caminho? |
| Custo | Número de passos do caminho encontrado |
| Nós Explorados | Nós retirados da fronteira |
| Nós Expandidos | Nós cujos vizinhos foram gerados |
| Pico da Fronteira | Tamanho máximo da fronteira durante a busca |
| Tempo de Execução | Tempo em milissegundos |
| Utilidade (J) | Métrica de desempenho ponderada |

---

## 6. Resultados

### Tabela Comparativa

| Algoritmo | Sucesso | Custo | Expandidos | Explorados | Fronteira | Tempo (ms) |
|-----------|---------|-------|------------|------------|-----------|------------|
| BFS | Sim | 45 | 132 | 133 | 6 | < 1 |
| DFS | Sim | 45 | 162 | 163 | 4 | < 1 |
| UCS | Sim | 45 | 132 | 133 | 6 | < 1 |
| Gulosa | Sim | 93 | 122 | 123 | 6 | < 1 |
| A* | Sim | 45 | 91 | 92 | 6 | < 1 |

### Análise dos Resultados

**Custo do Caminho:**
- BFS, DFS, UCS e A* encontraram caminhos de custo **45** — o caminho ótimo.
- DFS encontrou custo 45 neste labirinto específico, embora em geral não garanta otimalidade.
- A Busca Gulosa encontrou custo **93** — quase o dobro do ótimo. A heurística gulosa direciona o agente na direção do objetivo mas ignora o custo já acumulado, resultando em caminhos subótimos quando há desvios necessários.

**Nós Expandidos:**
- **A*** foi o mais eficiente com apenas **91 nós expandidos**, pois a combinação $f(n) = g(n) + h(n)$ foca a busca na direção correta sem desperdiçar expansões.
- A Busca Gulosa expandiu **122 nós** — menos que BFS/UCS, mas encontrou um caminho pior. Expandir menos nós não implica encontrar melhor caminho.
- **DFS** expandiu mais nós (**162**), pois pode explorar ramos profundos desnecessários antes de encontrar o objetivo.
- **BFS e UCS** tiveram desempenho idêntico (132 expandidos), o que é esperado com custos unitários.

**Pico da Fronteira:**
- Todos os algoritmos mantiveram fronteira pequena (4-6) devido à topologia estreita do labirinto com corredores.

---

## 7. Limitações

1. **Labirinto pequeno:** Com 17×25, as diferenças de desempenho entre algoritmos são sutis. Em labirintos maiores, as diferenças seriam mais expressivas.
2. **Custo unitário:** Com custos uniformes, BFS e UCS são equivalentes. Custos variáveis evidenciariam as vantagens do UCS.
3. **DFS com sorte:** O DFS encontrou o caminho ótimo neste labirinto, mas isso é específico desta topologia — em geral, DFS não garante otimalidade.

---

## 8. Conclusão

A implementação demonstrou que:

1. **A*** é o algoritmo mais eficiente globalmente — encontra o caminho ótimo com o menor número de nós expandidos (91), comprovando que a heurística de Manhattan é admissível e consistente para este domínio.

2. **BFS e UCS** produzem resultados idênticos com custo unitário, ambos encontrando o caminho ótimo.

3. **Busca Gulosa** é a mais rápida em termos de expansões mas sacrifica otimalidade — útil quando a velocidade importa mais que a qualidade da solução.

4. **DFS** é o menos previsível — pode encontrar o ótimo por coincidência, mas também pode explorar excessivamente.

A comparação entre os cinco algoritmos evidencia o **trade-off fundamental** entre completude, otimalidade e eficiência na busca em espaço de estados.
