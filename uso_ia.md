# Uso de Inteligência Artificial

Este documento detalha o uso de assistentes de Inteligência Artificial como ferramentas de apoio ao desenvolvimento, embasamento teórico, depuração e elaboração do relatório em todas as etapas do projeto.

## Ferramentas Utilizadas
* **Google Gemini (LLM):** Assistente conversacional utilizado para estruturação teórica, análise de dados, refatoração e elaboração das seções de Busca Clássica e Busca Local.
* **GitHub Copilot (Claude Opus 4):** Assistente de programação integrado ao VS Code, focado no desenvolvimento do módulo de Busca Online, geração de interfaces gráficas e depuração de código.

---

## 1. Busca Clássica

### Dúvidas e Conceitos Esclarecidos
* **Fronteira e Consumo de Memória:** A IA auxiliou no entendimento do conceito de "Pico de Fronteira" e como ele serve como uma métrica exata do consumo de RAM do computador durante a execução das buscas cegas e heurísticas.
* **Efeito Corredor:** Justificativa teórica do motivo de o Pico de Fronteira ter estacionado no valor 6 para todos os algoritmos, explicando como a topologia de corredores estreitos do mapa limitou o fator de ramificação.
* **Análise de Comportamento:** Esclarecimento sobre o comportamento matemático de cada algoritmo clássico no labirinto. Entendimento de por que a Busca Gulosa falhou de forma tão acentuada ao ficar presa em obstáculos (miopia) e como o $A^*$ conseguiu equilibrar otimalidade e eficiência usando a Distância de Manhattan.

### Correções e Geração de Código
* **Script Analítico (Python):** Geração do código independente `comparar_resultados.py`. O script usou a biblioteca *Matplotlib* para ler os resultados brutos da Busca Clássica e plotar um dashboard comparativo limpo, poupando o trabalho de gerar gráficos manualmente.
* **Correção de Bugs nos Resultados:** Auxílio para depurar e corrigir o código de formatação estrutural do relatório, resolvendo bugs de sobreposição e quebra de margens que afetavam a exibição das métricas e da tabela da Busca Clássica.

### Sugestões Rejeitadas e Validação
* **Sugestões:** Nenhuma sugestão principal foi rejeitada neste módulo.
* **Validação:** Todos os algoritmos foram testados no labirinto com resultados verificados manualmente.

### Exemplo de Prompt Utilizado
Na teoria eu sei que o BFS e o DFS usam uma 'fronteira', mas o que é isso na prática, dentro do código em Python? É uma lista, uma fila? Me explica como a fronteira funciona por trás dos panos enquanto o agente explora o labirinto.

#### Resposta do Gemini:
Excelente pergunta, cara! Falar de fronteira na teoria é uma coisa, mas ver o código rodando por trás dos panos é onde a mágica acontece.

Na prática, dentro do Python, a Fronteira é literalmente uma lista de coordenadas que guarda os lugares onde o agente já bateu o olho, mas ainda não pisou. É a "lista de tarefas pendentes" dele.

O que muda completamente de um algoritmo para o outro não é o que a fronteira guarda, mas de qual ponta da lista o algoritmo tira a próxima tarefa.

Aqui vai o raio-X do código em Python:

1. BFS (Busca em Largura) = FILA (Queue)
No BFS, a fronteira funciona como uma fila de banco: o primeiro que entra é o primeiro que sai (FIFO - First In, First Out).

No Python: A gente costuma usar a estrutura deque da biblioteca collections porque ela é super otimizada para tirar itens do começo.

Como funciona: Quando o agente vê caminhos novos, ele adiciona no final da fila (fronteira.append(vizinho)). Mas na hora de dar o próximo passo, ele tira o nó que está no início da fila (fronteira.popleft()).

O Efeito: Isso faz o agente explorar como uma poça d'água, varrendo tudo ao redor dele (os mais antigos na fila) antes de ir mais longe.

2. DFS (Busca em Profundidade) = PILHA (Stack)
No DFS, a fronteira funciona como uma pilha de pratos: o último prato que você colocou no topo é o primeiro que você tira para lavar (LIFO - Last In, First Out).

No Python: A gente usa uma simples e velha list padrão do Python.

Como funciona: Quando o agente vê caminhos novos, ele adiciona no final da lista (fronteira.append(vizinho)). Na hora de dar o próximo passo, ele também tira o nó do final da lista (fronteira.pop()).

O Efeito: Ele ignora as bifurcações antigas e vai "mergulhando" sempre na opção mais nova que acabou de descobrir, até bater a cara em um beco sem saída.

O "Loop" Mestre
Independente de ser BFS ou DFS, o esqueleto do código é quase sempre esse aqui:

Coloque a posição inicial (A) dentro da Fronteira.

Enquanto a Fronteira não estiver vazia, faça:

Tire um nó da Fronteira (É aqui que você usa pop() ou popleft()!)

É o objetivo (B)? Se sim, achou o caminho!

Se não for, marque como "visitado".

Olhe os vizinhos livres. Se não foram visitados e não estão na fronteira, jogue-os na Fronteira.

Repete!
---

## 2. Busca Local

### Entendimento de Código e Validação de Requisitos
* **Mapeamento do Código:** Identificação exata de onde o código original realizava ações teóricas (ex: geração da solução candidata inicial via `random.shuffle` e aplicação da função de custo baseada no UCS).
* **Descoberta Lógica:** Identificação de que o código original usava uma vizinhança "híbrida" (50% de chance de Swap e 50% de Inversão), o que foi ajustado para atender à regra do trabalho de escolher apenas uma técnica de perturbação.

### Tutoria em Conceitos Teóricos (Meta-heurísticas)
* **Tradução de Jargões:** Desmistificação de termos da Otimização Combinatória, esclarecendo que "Solução Candidata" é a ordem de visitação e que a "Vizinhança" é gerada por perturbações nessa ordem.
* **Passo a Passo Visual:** Entendimento da diferença exata entre a Troca Simples (Swap) e a Inversão de Trecho (2-opt / Reversal).
* **Vantagens e Desvantagens:** Discussão sobre como o Swap serve para "ajuste fino", enquanto a Inversão atua para desfazer rotas ruins que cruzam o próprio caminho.

### Modificação de Código e Estratégia de Testes
* **Refatoração Focada:** Alteração da função `gerar_vizinho` para aplicar estritamente a Inversão de Trecho, embasando a justificativa no relatório.
* **Engenharia de Testes:** Configuração do parâmetro `max_iteracoes` para forçar o Hill Climbing e o Simulated Annealing em cenários extremos, permitindo extrair dados práticos sobre as falhas e sucessos de cada método.

### Análise de Dados e Redação do Relatório Científico
* **Interpretação:** Análise dos *outputs* do terminal e curvas de convergência (taxas de sucesso de 100%, queda de temperatura, estabilização precoce).
* **Formulação e Lapidação:** Estruturação das respostas para as 6 questões de análise exigidas e compactação da análise sobre o "Compromisso entre Tempo e Qualidade" (Trade-off) em uma conclusão técnica fundamentada.

### Exemplo de Prompt Utilizado
Sobre os vizinhos ainda, eu não consegui entender da vizinhança por acaso seria o algoritmo encontrar outras formas de fazer uma rota ou determinar uma sequência? Teria como me mostra um exemplo passo a passo?

#### Resposta do Gemini:

O algoritmo não está tentando descobrir por quais corredores físicos o boneco deve passar para ir do ponto $A$ ao ponto $C_1$. O seu código já resolveu isso usando o UCS (Busca de Custo Uniforme) antes mesmo de a Busca Local começar! O UCS já sabe o caminho físico mais curto e o custo exato entre qualquer par de pontos.

O que o Hill Climbing e o Simulated Annealing fazem é apenas *mudar a ordem* dos checkpoints. A "vizinhança" é simplesmente o conjunto de todas as novas sequências que você pode formar fazendo uma pequena alteração na sequência atual.

---

### Exemplo Passo a Passo: A Vizinhança na Prática

Vamos imaginar um cenário reduzido. O agente sai de *A, precisa visitar *$C_1$*, *$C_2$* e *$C_3$*, e terminar em **B*.

#### Passo 1: A Solução Atual (O Chute Inicial)

O algoritmo embaralha os pontos e começa com esta sequência aleatória:

* *Sequência Atual:* [C1, C2, C3]
* *A Rota Completa fica:* $A \rightarrow C_1 \rightarrow C_2 \rightarrow C_3 \rightarrow B$
* *Custo Total (calculado pelo UCS):* 150 passos.

#### Passo 2: Gerando os "Vizinhos"

O algoritmo quer saber: "Tem algum caminho melhor perto daqui?". Ele vai usar a regra de vizinhança da *Troca Simples (Swap). Ou seja, ele vai gerar todas as combinações possíveis trocando apenas **dois* pontos de lugar na sequência atual.

Ele não tenta uma ordem totalmente nova. Ele apenas gera as "vizinhas":

* *Vizinho 1 (troca o 1º com o 2º):* [C2, C1, C3]
* Rota: $A \rightarrow C_2 \rightarrow C_1 \rightarrow C_3 \rightarrow B$
* Custo calculado: *170 passos* (Piorou!)


* *Vizinho 2 (troca o 2º com o 3º):* [C1, C3, C2]
* Rota: $A \rightarrow C_1 \rightarrow C_3 \rightarrow C_2 \rightarrow B$
* Custo calculado: *120 passos* (Melhorou!)


* *Vizinho 3 (troca o 1º com o 3º):* [C3, C2, C1]
* Rota: $A \rightarrow C_3 \rightarrow C_2 \rightarrow C_1 \rightarrow B$
* Custo calculado: *160 passos* (Piorou!)



#### Passo 3: A Decisão

O algoritmo analisa a vizinhança que acabou de criar. Ele percebe que o *Vizinho 2* ([C1, C3, C2]) custa apenas 120 passos, sendo muito melhor que a solução inicial de 150 passos.

O que ele faz? Ele descarta a solução antiga e a "Solução Atual" passa a ser o Vizinho 2.

#### Passo 4: O Ciclo Recomeça

Na próxima iteração, o algoritmo vai repetir o processo, mas agora o ponto de partida é a nova sequência: [C1, C3, C2]. Ele vai gerar os vizinhos desta nova sequência, testar os custos, pegar a melhor, e assim por diante.

---

## 3. Busca Online

### Dúvidas e Conceitos Esclarecidos
* **Lógica de Exploração:** Como implementar o ciclo *perceber → atualizar → planejar → agir* da busca online, separando corretamente o mapa real (simulador) do mapa interno (agente).
* **Heurística Otimista vs Pessimista:** Diferenciação no tratamento de células desconhecidas no $A^*$ parcial. Optou-se pela otimista (tratar `?` como livre) ao entender que a pessimista impediria o planejamento.
* **Raio de Percepção:** Funcionamento do raio de percepção usando Distância de Manhattan (formato losango) e seu impacto no número de replanejamentos.

### Geração de Código
* **Visualização com Pygame (`visualization.py`):** Geração da estrutura da interface colorida, sistema de controles interativos (SPACE, setas, HOME/END), renderização do mapa com névoa de guerra e legenda lateral.
* **Gráficos com Matplotlib (`graphs.py`):** Geração de 7 gráficos de desempenho (razão online/offline, movimentos, células reveladas vs revisitadas, replanejamentos, tempo, comparação geral, progressão de descoberta).
* **Módulo de Métricas (`metrics.py`):** Estruturação da coleta de métricas e exportação para CSV.

### Revisão de Código e Explicação de Erros
* **Debugging:** Identificação de um `IndexError` na função `_perceive()` causado por linhas do labirinto com comprimentos diferentes — corrigido com verificação de limites (*bounds*) e *padding*.
* **Depuração:** Compreensão de erros em tempo de execução e integração entre os módulos do sistema.

### Sugestões Rejeitadas e Validação
* **Sugestões:** Nenhuma sugestão principal foi rejeitada neste módulo.
* **Validação:** Todos os algoritmos foram testados manualmente. Os resultados experimentais foram comparados entre diferentes raios de percepção para confirmar a consistência. A razão online/offline do Replanning $A^*$ (1.06) foi rigorosamente verificada contra o caminho ótimo offline (custo 33 vs custo online 35).

### Exemplo de Prompt Utilizado
Me explique como funciona os sensores com a variância do local do raio

#### Resposta do Gemini:

Em resumo, há três razões distintas para o comportamento que vocês observaram:

Por que Custo Real e Revisitadas não mudam em nenhum dos dois algoritmos:

O raio r determina quando o agente percebe um obstáculo, não qual caminho ele percorre no final. O labirinto é fixo — as paredes estão nos mesmos lugares. No A*, o agente sempre converge para o mesmo caminho ótimo (custo 35), independente de descobrir as paredes cedo ou tarde. 

No DFS, a lógica de backtracking percorre as mesmas ramificações de qualquer forma, resultando nos mesmos 297 passos e 116 células revisitadas.

Por que os Replanejamentos do A caem com r maior:*
O replanning só é acionado quando o agente leva um susto — encontra uma parede que não estava no seu mapa interno.

 Com r=1 ele só enxerga os 4 vizinhos imediatos, então paredes mais distantes são surpresa frequente (14 replanejamentos). Com r=3 ele já inseriu essas paredes no mapa antes de chegar perto delas, então o plano atual já as contorna — menos surpresas, menos replanning (7).

Por que o DFS não muda nada mesmo com r maior:

O DFS não tem heurística nem usa o mapa para planejar adiante. 

Ele simplesmente mergulha em uma direção até bater, volta (backtrack) e tenta outra. Ver mais células ao redor com r=2 ou r=3 não altera essa lógica de exploração — a informação extra é percebida mas não aproveitada pelo algoritmo, então o comportamento final é estruturalmente idêntico para qualquer raio.