import csv
import os
import time
from maze import Maze
from classical_search import astar_offline
from online_search import ReplanningAStarAgent, OnlineDFSAgent


def run_experiment(maze_path, perception_radius=1):
    maze = Maze(maze_path)

    start_time = time.time()
    optimal_path, optimal_expanded, optimal_cost = astar_offline(maze, maze.start, maze.goal)
    offline_time = time.time() - start_time

    results = {
        'offline': {
            'success': optimal_path is not None,
            'cost': optimal_cost,
            'path_length': len(optimal_path) if optimal_path else 0,
            'expanded': optimal_expanded,
            'time': offline_time,
            'path': optimal_path
        }
    }

    start_time = time.time()
    agent_a = ReplanningAStarAgent(maze, perception_radius)
    metrics_a = agent_a.solve()
    time_a = time.time() - start_time

    ratio_a = metrics_a.real_cost / optimal_cost if optimal_cost > 0 else float('inf')

    results['replanning_astar'] = {
        'success': metrics_a.success,
        'total_movements': metrics_a.total_movements,
        'real_cost': metrics_a.real_cost,
        'cells_revealed': metrics_a.cells_revealed,
        'cells_revisited': metrics_a.cells_revisited,
        'replannings': metrics_a.replannings,
        'time': time_a,
        'online_offline_ratio': ratio_a,
        'path_taken': metrics_a.path_taken,
        'map_states': metrics_a.map_states,
        'visited_count': metrics_a.visited_count
    }

    start_time = time.time()
    agent_b = OnlineDFSAgent(maze, perception_radius)
    metrics_b = agent_b.solve()
    time_b = time.time() - start_time

    ratio_b = metrics_b.real_cost / optimal_cost if optimal_cost > 0 else float('inf')

    results['online_dfs'] = {
        'success': metrics_b.success,
        'total_movements': metrics_b.total_movements,
        'real_cost': metrics_b.real_cost,
        'cells_revealed': metrics_b.cells_revealed,
        'cells_revisited': metrics_b.cells_revisited,
        'replannings': metrics_b.replannings,
        'time': time_b,
        'online_offline_ratio': ratio_b,
        'path_taken': metrics_b.path_taken,
        'map_states': metrics_b.map_states,
        'visited_count': metrics_b.visited_count
    }

    return results


def run_multiple_radius_experiments(maze_path, radii=[1, 2, 3]):
    all_results = {}
    for r in radii:
        all_results[r] = run_experiment(maze_path, perception_radius=r)
    return all_results


def save_results_csv(results, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = []
    for radius, res in results.items():
        for algo_name in ['replanning_astar', 'online_dfs']:
            if algo_name in res:
                algo_res = res[algo_name]
                rows.append({
                    'raio_percepcao': radius,
                    'algoritmo': algo_name,
                    'sucesso': algo_res['success'],
                    'movimentos_totais': algo_res['total_movements'],
                    'custo_real': algo_res['real_cost'],
                    'celulas_reveladas': algo_res['cells_revealed'],
                    'celulas_revisitadas': algo_res['cells_revisited'],
                    'replanejamentos': algo_res['replannings'],
                    'tempo_execucao': f"{algo_res['time']:.6f}",
                    'razao_online_offline': f"{algo_res['online_offline_ratio']:.4f}",
                    'custo_otimo_offline': res['offline']['cost']
                })

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resultados salvos em: {output_path}")
