"""
Visualização do agente com Pygame — interface colorida.
Mostra o comportamento do agente passo a passo.
"""
import sys

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 200, 0)
RED = (220, 50, 50)
BLUE = (50, 100, 220)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
CYAN = (0, 200, 200)
PURPLE = (150, 50, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
FOG = (40, 40, 60)


CELL_SIZE = 35
FPS = 10


def visualize_online_search(map_states, optimal_path, maze_grid, title="Busca Online"):
    """
    Visualiza a busca online passo a passo com Pygame.
    """
    if not PYGAME_AVAILABLE:
        print("Pygame não disponível. Instale com: pip install pygame")
        return

    if not map_states:
        print("Sem estados para visualizar.")
        return

    rows = len(map_states[0]['map'])
    cols = len(map_states[0]['map'][0])

    width = cols * CELL_SIZE + 300  # espaço extra para info
    height = rows * CELL_SIZE + 60

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 14)
    font_large = pygame.font.SysFont('Consolas', 18, bold=True)

    state_idx = 0
    paused = False
    speed = FPS
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    state_idx = min(state_idx + 1, len(map_states) - 1)
                elif event.key == pygame.K_LEFT:
                    state_idx = max(state_idx - 1, 0)
                elif event.key == pygame.K_UP:
                    speed = min(speed + 5, 60)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed - 5, 1)
                elif event.key == pygame.K_HOME:
                    state_idx = 0
                elif event.key == pygame.K_END:
                    state_idx = len(map_states) - 1

        screen.fill(BLACK)

        state = map_states[state_idx]
        agent_pos = state['agent_pos']
        internal_map = state['map']
        goal = state['goal']

        # Desenha o mapa
        for r in range(rows):
            for c in range(cols):
                x = c * CELL_SIZE
                y = r * CELL_SIZE + 30

                cell = internal_map[r][c]

                if cell == '#':
                    color = DARK_GRAY
                elif cell == ' ':
                    # Célula livre conhecida
                    if (r, c) == goal:
                        color = RED
                    elif optimal_path and (r, c) in optimal_path:
                        color = LIGHT_GREEN
                    else:
                        color = WHITE
                else:  # '?'
                    color = FOG

                pygame.draw.rect(screen, color, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))

                # Marca o caminho percorrido até agora
                path_up_to_now = []
                for s in map_states[:state_idx + 1]:
                    path_up_to_now.append(s['agent_pos'])

                if (r, c) in path_up_to_now and (r, c) != agent_pos:
                    pygame.draw.circle(screen, CYAN,
                                       (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 5)

        # Desenha o agente
        ax = agent_pos[1] * CELL_SIZE
        ay = agent_pos[0] * CELL_SIZE + 30
        pygame.draw.circle(screen, YELLOW,
                           (ax + CELL_SIZE // 2, ay + CELL_SIZE // 2),
                           CELL_SIZE // 3)

        # Desenha o objetivo
        gx = goal[1] * CELL_SIZE
        gy = goal[0] * CELL_SIZE + 30
        pygame.draw.rect(screen, RED, (gx + 5, gy + 5, CELL_SIZE - 11, CELL_SIZE - 11), 3)

        # Painel de informações
        info_x = cols * CELL_SIZE + 20
        info_y = 40

        title_surf = font_large.render(title, True, WHITE)
        screen.blit(title_surf, (info_x, info_y))
        info_y += 30

        info_lines = [
            f"Passo: {state_idx + 1}/{len(map_states)}",
            f"Posição: ({agent_pos[0]}, {agent_pos[1]})",
            f"Velocidade: {speed} FPS",
            "",
            "Controles:",
            "SPACE - Pausar/Continuar",
            "← → - Passo anterior/próximo",
            "↑ ↓ - Aumentar/Diminuir vel.",
            "HOME - Início",
            "END - Fim",
            "ESC - Sair",
            "",
            "Legenda:",
        ]

        for line in info_lines:
            surf = font.render(line, True, WHITE)
            screen.blit(surf, (info_x, info_y))
            info_y += 20

        # Legenda colorida
        legend_items = [
            (YELLOW, "Agente"),
            (RED, "Objetivo (B)"),
            (WHITE, "Livre (conhecido)"),
            (FOG, "Desconhecido (?)"),
            (DARK_GRAY, "Parede (#)"),
            (CYAN, "Caminho percorrido"),
            (LIGHT_GREEN, "Caminho ótimo offline"),
        ]

        for color, label in legend_items:
            pygame.draw.rect(screen, color, (info_x, info_y, 15, 15))
            surf = font.render(f"  {label}", True, WHITE)
            screen.blit(surf, (info_x + 18, info_y))
            info_y += 22

        # Status
        info_y += 10
        status = "PAUSADO" if paused else "EXECUTANDO"
        status_color = ORANGE if paused else GREEN
        surf = font.render(f"Status: {status}", True, status_color)
        screen.blit(surf, (info_x, info_y))

        pygame.display.flip()

        # Avança automaticamente se não pausado
        if not paused and state_idx < len(map_states) - 1:
            state_idx += 1

        clock.tick(speed)

    pygame.quit()


def visualize_comparison(results, maze):
    """
    Visualização estática comparando os caminhos dos algoritmos.
    """
    if not PYGAME_AVAILABLE:
        print("Pygame não disponível.")
        return

    rows = maze.rows
    cols = maze.cols
    width = cols * CELL_SIZE * 2 + 40
    height = rows * CELL_SIZE + 100

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Comparação: Replanning A* vs Online DFS")
    font = pygame.font.SysFont('Consolas', 14)
    font_large = pygame.font.SysFont('Consolas', 16, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BLACK)

        offset_x = [10, cols * CELL_SIZE + 30]
        titles = ["Replanning A*", "Online DFS"]
        keys = ['replanning_astar', 'online_dfs']

        for idx, (ox, algo_title, key) in enumerate(zip(offset_x, titles, keys)):
            # Título
            surf = font_large.render(algo_title, True, WHITE)
            screen.blit(surf, (ox, 5))

            path_set = set(results[key]['path_taken']) if results[key]['success'] else set()
            optimal_set = set(results['offline']['path']) if results['offline']['path'] else set()

            for r in range(rows):
                for c in range(cols):
                    x = ox + c * CELL_SIZE
                    y = r * CELL_SIZE + 30

                    if maze.grid[r][c] == '#':
                        color = DARK_GRAY
                    elif (r, c) in path_set:
                        color = CYAN
                    elif (r, c) in optimal_set:
                        color = LIGHT_GREEN
                    else:
                        color = WHITE

                    pygame.draw.rect(screen, color, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))

            # Start/Goal markers
            sx, sy = maze.start
            gx, gy = maze.goal
            pygame.draw.circle(screen, GREEN,
                               (ox + sy * CELL_SIZE + CELL_SIZE // 2,
                                sx * CELL_SIZE + 30 + CELL_SIZE // 2), 8)
            pygame.draw.circle(screen, RED,
                               (ox + gy * CELL_SIZE + CELL_SIZE // 2,
                                gx * CELL_SIZE + 30 + CELL_SIZE // 2), 8)

            # Métricas
            res = results[key]
            info_y = rows * CELL_SIZE + 40
            info_text = f"Custo: {res['real_cost']} | Razão: {res['online_offline_ratio']:.2f} | Revisitas: {res['cells_revisited']}"
            surf = font.render(info_text, True, WHITE)
            screen.blit(surf, (ox, info_y))

        pygame.display.flip()

    pygame.quit()
