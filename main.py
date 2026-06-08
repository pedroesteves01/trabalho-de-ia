import sys
import os

from maze import Maze
from classical_search import astar_offline
from online_search import ReplanningAStarAgent, OnlineDFSAgent
from metrics import run_experiment, run_multiple_radius_experiments, save_results_csv
from graphs import generate_all_graphs
from visualization import visualize_online_search, visualize_comparison, PYGAME_AVAILABLE


MAZE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lab3.txt')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
GRAPHS_DIR = os.path.join(RESULTS_DIR, 'graphs')


def print_banner():
    print("=" * 70)
    print("  BUSCA ONLINE NO LABIRINTO DESCONHECIDO")
    print("  Trabalho Prático — Parte IV (Semana 3)")
    print("  Agente Inteligente com Modelo Interno")
    print("=" * 70)
    print()


def print_results(results):
    offline = results['offline']
    print(f"  ┌─ CAMINHO ÓTIMO OFFLINE (A*)")
    print(f"  │  Sucesso: {offline['success']}")
    print(f"  │  Custo: {offline['cost']}")
    print(f"  │  Tamanho do caminho: {offline['path_length']}")
    print(f"  │  Nós expandidos: {offline['expanded']}")
    print(f"  │  Tempo: {offline['time']*1000:.2f} ms")
    print(f"  └────────────────────────────────")
    print()

    for algo_name, label in [('replanning_astar', 'REPLANNING A*'),
                              ('online_dfs', 'ONLINE DFS')]:
        res = results[algo_name]
        print(f"  ┌─ {label}")
        print(f"  │  Sucesso: {res['success']}")
        print(f"  │  Movimentos totais: {res['total_movements']}")
        print(f"  │  Custo real: {res['real_cost']}")
        print(f"  │  Células reveladas: {res['cells_revealed']}")
        print(f"  │  Células revisitadas: {res['cells_revisited']}")
        print(f"  │  Replanejamentos: {res['replannings']}")
        print(f"  │  Tempo: {res['time']*1000:.2f} ms")
        print(f"  │  Razão online/offline: {res['online_offline_ratio']:.4f}")
        print(f"  └────────────────────────────────")
        print()


def main():
    args = sys.argv[1:]
    no_viz = '--no-viz' in args
    viz_only = '--viz-only' in args
    algo_filter = None
    if '--algo' in args:
        idx = args.index('--algo')
        if idx + 1 < len(args):
            algo_filter = args[idx + 1]

    print_banner()

    print(f"[1] Carregando labirinto: {MAZE_FILE}")
    maze = Maze(MAZE_FILE)
    print(f"    Dimensões: {maze.rows} x {maze.cols}")
    print(f"    Início (A): {maze.start}")
    print(f"    Objetivo (B): {maze.goal}")
    print()

    if not viz_only:
        print("[2] Executando experimentos...")
        radii = [1, 2, 3]
        all_results = run_multiple_radius_experiments(MAZE_FILE, radii)

        print("\n  === RESULTADOS (Raio de Percepção = 1) ===\n")
        print_results(all_results[1])

        print("\n  === RESULTADOS (Raio de Percepção = 2) ===\n")
        print_results(all_results[2])

        print("\n  === RESULTADOS (Raio de Percepção = 3) ===\n")
        print_results(all_results[3])

        print("[3] Salvando resultados experimentais...")
        os.makedirs(RESULTS_DIR, exist_ok=True)
        save_results_csv(all_results, os.path.join(RESULTS_DIR, 'resultados_experimentais.csv'))

        print("\n[4] Gerando gráficos de desempenho...")
        generate_all_graphs(all_results, GRAPHS_DIR)

        results_r1 = all_results[1]
    else:
        results_r1 = run_experiment(MAZE_FILE, perception_radius=1)

    if not no_viz and PYGAME_AVAILABLE:
        print("\n[5] Iniciando visualização interativa...")
        print("    (Pressione SPACE para pausar, ← → para navegar, ESC para sair)")

        optimal_path_set = set(results_r1['offline']['path']) if results_r1['offline']['path'] else set()

        if algo_filter != 'dfs':
            visualize_online_search(
                results_r1['replanning_astar']['map_states'],
                optimal_path_set,
                maze.grid,
                title="Replanning A* — Busca Online"
            )

        if algo_filter != 'replanning':
            visualize_online_search(
                results_r1['online_dfs']['map_states'],
                optimal_path_set,
                maze.grid,
                title="Online DFS — Busca Online"
            )
    elif not PYGAME_AVAILABLE and not no_viz:
        print("\n[!] Pygame não instalado. Execute: pip install pygame")
        print("    Os gráficos e resultados CSV foram gerados com sucesso.")

    print("\n" + "=" * 70)
    print("  Execução concluída!")
    print(f"  Resultados em: {RESULTS_DIR}")
    print(f"  Gráficos em: {GRAPHS_DIR}")
    print("=" * 70)


if __name__ == '__main__':
    main()
