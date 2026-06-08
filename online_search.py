from maze import AgentMap
from classical_search import astar_on_partial_map


class OnlineSearchMetrics:

    def __init__(self):
        self.success = False
        self.total_movements = 0
        self.real_cost = 0
        self.cells_revealed = 0
        self.cells_revisited = 0
        self.replannings = 0
        self.path_taken = []
        self.visited_count = {}
        self.map_states = [] 


class OnlineAgent:

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
        self._perceive()

    def _perceive(self):
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
        self.current_pos = next_pos
        self.metrics.total_movements += 1
        self.metrics.real_cost += 1
        self.metrics.path_taken.append(next_pos)

        if next_pos in self.metrics.visited_count:
            self.metrics.visited_count[next_pos] += 1
            self.metrics.cells_revisited += 1
        else:
            self.metrics.visited_count[next_pos] = 1

        self._perceive()

    def _save_state(self):
        state = {
            'agent_pos': self.current_pos,
            'map': [row[:] for row in self.agent_map.grid],
            'goal': self.goal
        }
        self.metrics.map_states.append(state)


class ReplanningAStarAgent(OnlineAgent):

    def solve(self):
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

            for i in range(1, len(path)):
                next_pos = path[i]

                if self.real_maze.is_free(next_pos):
                    self._move_to(next_pos)
                    self._save_state()

                    if self.current_pos == self.goal:
                        self.metrics.success = True
                        return self.metrics
                else:
                    # Descobriu parede — atualiza mapa e replaneja rota
                    self.agent_map.update(next_pos, AgentMap.WALL)
                    self.metrics.cells_revealed += 1
                    break 

        if self.current_pos == self.goal:
            self.metrics.success = True
        else:
            self.metrics.success = False

        return self.metrics


class OnlineDFSAgent(OnlineAgent):

    def solve(self):
        self._save_state()
        visited = {self.current_pos}
        stack = [self.current_pos]
        untried = {}
        unbacktracked = {}

        max_steps = self.real_maze.rows * self.real_maze.cols * 4

        while self.current_pos != self.goal and self.metrics.total_movements < max_steps:
            if self.current_pos == self.goal:
                break

            if self.current_pos not in untried:
                neighbors = []
                r, c = self.current_pos
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if self.real_maze.is_free((nr, nc)):
                        neighbors.append((nr, nc))
                untried[self.current_pos] = [n for n in neighbors if n not in visited]

            if untried[self.current_pos]:
                next_pos = untried[self.current_pos].pop(0)
                visited.add(next_pos)
                stack.append(next_pos)

                if next_pos not in unbacktracked:
                    unbacktracked[next_pos] = []
                unbacktracked[next_pos].append(self.current_pos)

                self._move_to(next_pos)
                self._save_state()
                self.metrics.replannings += 1

            elif self.current_pos in unbacktracked and unbacktracked[self.current_pos]:
                next_pos = unbacktracked[self.current_pos].pop()
                if stack:
                    stack.pop()
                self._move_to(next_pos)
                self._save_state()
                self.metrics.replannings += 1
            else:
                break

        if self.current_pos == self.goal:
            self.metrics.success = True
        else:
            self.metrics.success = False

        return self.metrics
