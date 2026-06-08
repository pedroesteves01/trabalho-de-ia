import heapq
import itertools
import math


def manhattan_distance(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar_offline(maze, start, goal):

    contador = itertools.count()
    fronteira = []
    g_inicio = 0.0
    f_inicio = g_inicio + manhattan_distance(start, goal)
    heapq.heappush(fronteira, (f_inicio, next(contador), start, g_inicio))
    came_from = {}
    melhor_g = {start: 0.0}
    fechados = set()
    nos_explorados = 0
    nos_expandidos = 0

    while fronteira:
        f_val, _, current, current_g = heapq.heappop(fronteira)

        if current in fechados:
            continue

        nos_explorados += 1

        if current == goal:
            path = _reconstruct_path(came_from, current)
            return path, nos_expandidos, int(current_g)

        fechados.add(current)
        nos_expandidos += 1

        for neighbor in maze.get_neighbors(current):
            novo_g = current_g + 1
            if neighbor in fechados:
                continue
            if novo_g < melhor_g.get(neighbor, math.inf):
                came_from[neighbor] = current
                melhor_g[neighbor] = novo_g
                f_neighbor = novo_g + manhattan_distance(neighbor, goal)
                heapq.heappush(fronteira, (f_neighbor, next(contador), neighbor, novo_g))

    return None, nos_expandidos, float('inf')


def astar_on_partial_map(agent_map, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    expanded = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        expanded += 1

        if current == goal:
            path = _reconstruct_path(came_from, current)
            return path, expanded

        for neighbor in agent_map.get_passable_neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, expanded


def _reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
