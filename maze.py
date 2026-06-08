class Maze:

    WALL = '#'
    FREE = ' '
    START = 'A'
    GOAL = 'B'
    UNKNOWN = '?'

    def __init__(self, filepath):
        self.grid = []
        self.start = None
        self.goal = None
        self.rows = 0
        self.cols = 0
        self._load(filepath)

    def _load(self, filepath):
        with open(filepath, 'r') as f:
            for row_idx, line in enumerate(f):
                line = line.rstrip('\n').rstrip('\r')
                if not line:
                    continue
                row = []
                for col_idx, ch in enumerate(line):
                    if ch == self.START:
                        self.start = (row_idx, col_idx)
                        row.append(self.FREE)
                    elif ch == self.GOAL:
                        self.goal = (row_idx, col_idx)
                        row.append(self.FREE)
                    elif ch == self.UNKNOWN:
                        row.append(self.FREE)
                    else:
                        row.append(ch)
                self.grid.append(row)
        self.rows = len(self.grid)
        self.cols = max(len(row) for row in self.grid) if self.rows > 0 else 0
        for row in self.grid:
            while len(row) < self.cols:
                row.append(self.WALL)

    def is_free(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < len(self.grid[r]):
            return self.grid[r][c] != self.WALL
        return False

    def get_neighbors(self, pos):
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_free((nr, nc)):
                neighbors.append((nr, nc))
        return neighbors


class AgentMap:
    WALL = '#'
    FREE = ' '
    UNKNOWN = '?'

    def __init__(self, rows, cols, start_pos):
        self.grid = [[self.UNKNOWN for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.start = start_pos
        self.grid[start_pos[0]][start_pos[1]] = self.FREE

    def update(self, pos, cell_type):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = cell_type

    def is_known(self, pos):
        r, c = pos
        return self.grid[r][c] != self.UNKNOWN

    def is_free(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == self.FREE
        return False

    def is_unknown(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == self.UNKNOWN
        return False

    def get_known_neighbors(self, pos):
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_free((nr, nc)):
                neighbors.append((nr, nc))
        return neighbors

    def get_passable_neighbors(self, pos):
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != self.WALL:
                    neighbors.append((nr, nc))
        return neighbors
