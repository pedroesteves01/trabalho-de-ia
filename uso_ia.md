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