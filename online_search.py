"""
Algoritmos de busca online no labirinto desconhecido.
Implementa:
  - Opção A: Replanning com A*
  - Opção B: Online DFS
"""
from maze import AgentMap
from classical_search import astar_on_partial_map


class OnlineSearchMetrics:
    """Coleta métricas da busca online."""

    def __init__(self):
        self.success = False
        self.total_movements = 0
        self.real_cost = 0
        self.cells_revealed = 0
        self.cells_revisited = 0
        self.replannings = 0
        self.path_taken = []
        self.visited_count = {}
        self.map_states = []  # snapshots do mapa para visualização


class OnlineAgent:
    """Agente de busca online base."""

    def __init__(self, real_maze, perception_radius=1):
        self.real_maze = real_maze
        self.start = real_maze.start
        self.goal = real_maze.goal
        self.perception_radius = perception_radius
        self.agent_map = AgentMap(real_maze.rows, real_maze.cols, self.start)
        self.current_pos = self.start
        self.metrics = OnlineSearchMetrics()
        self.metrics.path_taken.append(self.start)
        self.metrics.visited_count[self.start] = 1
        # Percepção inicial
        self._perceive()

    def _perceive(self):
        """O agente percebe células na vizinhança (raio r)."""
        r, c = self.current_pos
        for dr in range(-self.perception_radius, self.perception_radius + 1):
            for dc in range(-self.perception_radius, self.perception_radius + 1):
                if abs(dr) + abs(dc) <= self.perception_radius:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.real_maze.rows and
                            0 <= nc < self.real_maze.cols and
                            nc < len(self.real_maze.grid[nr])):
                        if not self.agent_map.is_known((nr, nc)):
                            self.metrics.cells_revealed += 1
                        if self.real_maze.is_free((nr, nc)):
                            self.agent_map.update((nr, nc), AgentMap.FREE)
                        else:
                            self.agent_map.update((nr, nc), AgentMap.WALL)

    def _move_to(self, next_pos):
        """Move o agente para a próxima posição."""
        self.current_pos = next_pos
        self.metrics.total_movements += 1
        self.metrics.real_cost += 1
        self.metrics.path_taken.append(next_pos)

        # Contabilizar revisitas
        if next_pos in self.metrics.visited_count:
            self.metrics.visited_count[next_pos] += 1
            self.metrics.cells_revisited += 1
        else:
            self.metrics.visited_count[next_pos] = 1

        # Percepção após mover
        self._perceive()

    def _save_state(self):
        """Salva snapshot do mapa interno para visualização."""
        state = {
            'agent_pos': self.current_pos,
            'map': [row[:] for row in self.agent_map.grid],
            'goal': self.goal
        }
        self.metrics.map_states.append(state)


class ReplanningAStarAgent(OnlineAgent):
    """
    Opção A: Replanning com A*.
    A cada passo, executa A* no mapa parcial e segue o próximo passo.
    """

    def solve(self):
        """Executa a busca online com replanning."""
        self._save_state()
        max_steps = self.real_maze.rows * self.real_maze.cols * 4  # limite de segurança

        while self.current_pos != self.goal and self.metrics.total_movements < max_steps:
            # Planeja caminho com A* no mapa parcial
            result = astar_on_partial_map(self.agent_map, self.current_pos, self.goal)
            self.metrics.replannings += 1

            if result[0] is None:
                # Sem caminho encontrado — falha
                self.metrics.success = False
                return self.metrics

            path = result[0]

            if len(path) < 2:
                break

            # Tenta seguir o caminho planejado
            for i in range(1, len(path)):
                next_pos = path[i]

                # Verifica se o próximo passo é realmente livre no mapa real
                if self.real_maze.is_free(next_pos):
                    self._move_to(next_pos)
                    self._save_state()

                    if self.current_pos == self.goal:
                        self.metrics.success = True
                        return self.metrics
                else:
                    # Descobriu parede — atualiza mapa e replaneja
                    self.agent_map.update(next_pos, AgentMap.WALL)
                    self.metrics.cells_revealed += 1
                    break  # Sai do loop para replanejar

        if self.current_pos == self.goal:
            self.metrics.success = True
        else:
            self.metrics.success = False

        return self.metrics


class OnlineDFSAgent(OnlineAgent):
    """
    Opção B: Online DFS.
    Explora sistematicamente mantendo estados visitados e caminho de retorno.
    """

    def solve(self):
        """Executa a busca online com DFS."""
        self._save_state()
        visited = {self.current_pos}
        stack = [self.current_pos]
        # Ações não testadas por estado
        untried = {}
        # Mapeamento de retorno
        unbacktracked = {}

        max_steps = self.real_maze.rows * self.real_maze.cols * 4

        while self.current_pos != self.goal and self.metrics.total_movements < max_steps:
            if self.current_pos == self.goal:
                break

            # Inicializa ações não testadas para o estado atual
            if self.current_pos not in untried:
                neighbors = []
                r, c = self.current_pos
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if self.real_maze.is_free((nr, nc)):
                        neighbors.append((nr, nc))
                untried[self.current_pos] = [n for n in neighbors if n not in visited]

            if untried[self.current_pos]:
                # Há vizinhos não visitados — avança
                next_pos = untried[self.current_pos].pop(0)
                visited.add(next_pos)
                stack.append(next_pos)

                # Registra caminho de retorno
                if next_pos not in unbacktracked:
                    unbacktracked[next_pos] = []
                unbacktracked[next_pos].append(self.current_pos)

                self._move_to(next_pos)
                self._save_state()
                self.metrics.replannings += 1

            elif self.current_pos in unbacktracked and unbacktracked[self.current_pos]:
                # Backtrack — volta pelo caminho
                next_pos = unbacktracked[self.current_pos].pop()
                if stack:
                    stack.pop()
                self._move_to(next_pos)
                self._save_state()
                self.metrics.replannings += 1
            else:
                # Sem saída — falha
                break

        if self.current_pos == self.goal:
            self.metrics.success = True
        else:
            self.metrics.success = False

        return self.metrics
