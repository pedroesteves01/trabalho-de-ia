# Relatório Técnico — Busca Local no Labirinto com Pontos de Coleta

## Trabalho Prático — Parte III (Semana 2)
**Curso:** Engenharia de Computação / Sistemas de Informação  
**Linguagem:** Python  
**Tema:** Otimização de Rotas com Busca Local

---

## 1. Introdução

Este relatório apresenta a implementação e análise da **Parte III** do trabalho prático: a **Busca Local para Otimização de Rotas em Labirinto**. Nesta etapa, o agente deve visitar **todos os pontos de coleta** (C1, C2, C3) no labirinto antes de chegar ao destino final (B), minimizando o custo total do percurso.

O problema consiste em encontrar a **melhor ordem de visita** aos checkpoints, configurando um problema de otimização combinatória análogo ao **Problema do Caixeiro Viajante (TSP)**. Foram implementados dois algoritmos de busca local:
- **Hill Climbing** (Subida de Encosta)
- **Simulated Annealing** (Recozimento Simulado)

---

## 2. Modelagem PEAS

### Performance
A medida de desempenho é o **custo total do percurso** em passos:

$$\text{custo}(\pi) = d(A, C_{\pi(1)}) + \sum_{i=1}^{k-1} d(C_{\pi(i)}, C_{\pi(i+1)}) + d(C_{\pi(k)}, B)$$

Onde $\pi$ é uma permutação dos checkpoints e $d(p, q)$ é a distância real pelo labirinto (calculada via UCS).

### Environment
- Labirinto 19×33 em grade discreta (`lab2.txt`)
- Células livres, paredes (`#`), posição inicial (`A`), destino (`B`)
- **3 checkpoints** de coleta: C1, C2, C3
- **Completamente observável** — o agente conhece o mapa completo
- **Determinístico** e **estático**

### Actuators
O agente não se move diretamente — ele escolhe a **ordem de visita** dos checkpoints. O movimento físico é calculado via UCS entre pontos.

### Sensors
Percepção global — o agente conhece toda a estrutura do labirinto e as posições de todos os pontos.

---

## 3. Formulação Formal do Problema

O problema de otimização é formulado como:

$$\langle \Sigma, f, N \rangle$$

Onde:
- $\Sigma$: espaço de soluções — todas as permutações $\pi$ de $\{C1, C2, C3\}$ ($3! = 6$ permutações)
- $f: \Sigma \rightarrow \mathbb{R}$: função de custo — custo total do percurso $A \rightarrow C_{\pi(1)} \rightarrow \ldots \rightarrow C_{\pi(k)} \rightarrow B$
- $N: \Sigma \rightarrow 2^{\Sigma}$: função de vizinhança — swap aleatório de dois checkpoints ou reversão de segmento (2-opt)

**Objetivo:** Encontrar $\pi^* = \arg\min_{\pi \in \Sigma} f(\pi)$

---

## 4. Descrição dos Algoritmos

### 4.1 Hill Climbing (Subida de Encosta)

Algoritmo de busca local que aceita apenas vizinhos com custo **igual ou menor** ao atual.

**Parâmetros:**
- Iterações máximas: 1000

**Procedimento:**
1. Gera solução inicial aleatória (permutação dos checkpoints)
2. Gera vizinho (swap ou 2-opt)
3. Se $f(\text{vizinho}) \leq f(\text{atual})$: aceita
4. Repete até atingir limite de iterações

**Limitação:** Pode ficar preso em **mínimos locais** — quando nenhum vizinho melhora a solução atual, o algoritmo estagna.

### 4.2 Simulated Annealing (Recozimento Simulado)

Algoritmo que aceita soluções piores com probabilidade decrescente, permitindo escapar de mínimos locais.

**Parâmetros:**
- Temperatura inicial: $T_0 = 10000$
- Taxa de resfriamento: $\alpha = 0.95$
- Temperatura mínima: $T_{min} = 0.1$

**Procedimento:**
1. Gera solução inicial aleatória
2. Gera vizinho e calcula $\Delta = f(\text{vizinho}) - f(\text{atual})$
3. Se $\Delta < 0$: aceita (melhora)
4. Se $\Delta \geq 0$: aceita com probabilidade $P = e^{-\Delta / T}$
5. Reduz temperatura: $T \leftarrow \alpha \cdot T$
6. Repete até $T < T_{min}$

### 4.3 Função de Vizinhança

A vizinhança é gerada por duas operações escolhidas aleatoriamente (50% cada):
- **Swap:** troca a posição de dois checkpoints na ordem
- **2-opt:** inverte um segmento da sequência de visita

### 4.4 Pré-computação de Rotas

Antes de executar os algoritmos de busca local, o sistema pré-computa as **distâncias e caminhos exatos** entre todos os pares de pontos importantes (A, C1, C2, C3, B) usando **UCS (Busca de Custo Uniforme)**. Isso permite que a função de custo $f(\pi)$ seja avaliada em $O(k)$ usando apenas consultas ao dicionário, sem recalcular caminhos durante a otimização.

---

## 5. Metodologia Experimental

### Configuração
- **Labirinto:** `lab2.txt` (19×33 com corredores e checkpoints)
- **Posição inicial:** $A = (1, 1)$
- **Posição objetivo:** $B = (17, 30)$
- **Checkpoints:** C1 = $(1, 30)$, C2 = $(13, 10)$, C3 = $(17, 4)$
- **Número de execuções:** 30 por algoritmo

### Métricas Coletadas
| Métrica | Descrição |
|---------|-----------|
| Melhor custo | Menor custo encontrado nas 30 execuções |
| Pior custo | Maior custo encontrado nas 30 execuções |
| Custo médio | Média dos custos nas 30 execuções |
| Tempo médio | Tempo médio de execução |
| Iterações médias | Número médio de iterações por execução |
| Taxa de sucesso | Percentual de execuções que atingiram o melhor custo global |

---

## 6. Resultados

### Tabela Comparativa (30 Execuções)

| Métrica | Hill Climbing | Simulated Annealing |
|---------|--------------|-------------------- |
| Melhor custo | 233 passos | 233 passos |
| Pior custo | 233 passos | 233 passos |
| Custo médio | 233.00 passos | 233.00 passos |
| Tempo médio | 0.0021 s | 0.0005 s |
| Iterações médias | 1000.0 | 225.0 |
| Taxa de sucesso | 100.00% | 100.00% |

### Análise dos Resultados

**Convergência Total:** Ambos os algoritmos encontraram o custo ótimo de **233 passos** em 100% das execuções. Isso é explicado pelo tamanho muito pequeno do espaço de busca — com apenas 3 checkpoints, existem $3! = 6$ permutações possíveis, tornando trivial encontrar o ótimo.

**Rota Ótima:** A sequência que minimiza o custo total é $A \rightarrow C_{\pi(1)} \rightarrow C_{\pi(2)} \rightarrow C_{\pi(3)} \rightarrow B$, totalizando 233 passos pelo labirinto.

**Tempo de Execução:** O Simulated Annealing foi mais rápido (0.0005s vs 0.0021s) por ter convergido em apenas 225 iterações (determinado pelo schedule de temperatura), enquanto o Hill Climbing executa todas as 1000 iterações fixas.

**Observação sobre o espaço de busca:** Com 3 checkpoints, o problema é pequeno demais para evidenciar as vantagens do Simulated Annealing sobre o Hill Climbing. Com mais checkpoints (e.g., 10+), o espaço cresce fatorialmente e o SA teria vantagem por escapar de mínimos locais.

---

## 7. Limitações

1. **Espaço de busca pequeno:** Com 3 checkpoints ($3! = 6$ permutações), ambos os algoritmos encontram trivialmente o ótimo. A real vantagem do Simulated Annealing seria visível com mais checkpoints.
2. **Sem custos variáveis:** Todos os movimentos têm custo 1. Custos variáveis (terreno, peso) aumentariam a complexidade da otimização.
3. **Sem restrições temporais:** Não há janelas de tempo ou prioridades nos pontos de coleta.

---

## 8. Conclusão

A implementação demonstrou que:

1. **Ambos os algoritmos** encontram consistentemente o custo ótimo de 233 passos, com taxa de sucesso de 100% em 30 execuções.

2. **Simulated Annealing** converge mais rapidamente (225 iterações vs 1000) graças ao schedule de temperatura que naturalmente encerra a busca quando a temperatura atinge 0.1.

3. A **pré-computação de rotas via UCS** é essencial para eficiência — permite avaliar cada permutação em tempo constante sem recalcular caminhos no labirinto.

4. Para instâncias maiores do problema (mais checkpoints), espera-se que o SA supere o HC por sua capacidade de escapar de mínimos locais através da aceitação probabilística de soluções piores.
