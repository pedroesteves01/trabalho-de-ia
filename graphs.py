"""
Geração de gráficos de desempenho para a busca online.
"""
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para salvar imagens


def generate_all_graphs(results_by_radius, output_dir):
    """Gera todos os gráficos de desempenho."""
    os.makedirs(output_dir, exist_ok=True)

    # Gráfico 1: Razão online/offline por raio de percepção
    plot_ratio_by_radius(results_by_radius, output_dir)

    # Gráfico 2: Movimentos totais por algoritmo e raio
    plot_movements_by_radius(results_by_radius, output_dir)

    # Gráfico 3: Células reveladas vs revisitadas
    plot_revealed_vs_revisited(results_by_radius, output_dir)

    # Gráfico 4: Replanejamentos por raio
    plot_replannings(results_by_radius, output_dir)

    # Gráfico 5: Tempo de execução
    plot_execution_time(results_by_radius, output_dir)

    # Gráfico 6: Comparação geral (barras)
    plot_comparison_bars(results_by_radius, output_dir)

    # Gráfico 7: Progressão de descoberta do mapa (para raio=1)
    if 1 in results_by_radius:
        plot_discovery_progression(results_by_radius[1], output_dir)

    print(f"Gráficos salvos em: {output_dir}")


def plot_ratio_by_radius(results, output_dir):
    """Razão online/offline por raio de percepção."""
    radii = sorted(results.keys())
    ratio_astar = [results[r]['replanning_astar']['online_offline_ratio'] for r in radii]
    ratio_dfs = [results[r]['online_dfs']['online_offline_ratio'] for r in radii]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(radii))
    width = 0.35

    bars1 = ax.bar([i - width/2 for i in x], ratio_astar, width, label='Replanning A*', color='#2196F3')
    bars2 = ax.bar([i + width/2 for i in x], ratio_dfs, width, label='Online DFS', color='#FF9800')

    ax.set_xlabel('Raio de Percepção')
    ax.set_ylabel('Razão Online/Offline')
    ax.set_title('Razão Online/Offline por Raio de Percepção')
    ax.set_xticks(x)
    ax.set_xticklabels(radii)
    ax.axhline(y=1.0, color='green', linestyle='--', label='Ótimo (razão = 1.0)')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Adiciona valores nas barras
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'razao_online_offline.png'), dpi=150)
    plt.close()


def plot_movements_by_radius(results, output_dir):
    """Movimentos totais por raio de percepção."""
    radii = sorted(results.keys())
    mov_astar = [results[r]['replanning_astar']['total_movements'] for r in radii]
    mov_dfs = [results[r]['online_dfs']['total_movements'] for r in radii]
    optimal = [results[radii[0]]['offline']['cost']] * len(radii)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(radii, mov_astar, 'o-', color='#2196F3', linewidth=2, markersize=8, label='Replanning A*')
    ax.plot(radii, mov_dfs, 's-', color='#FF9800', linewidth=2, markersize=8, label='Online DFS')
    ax.plot(radii, optimal, '--', color='green', linewidth=2, label='Custo Ótimo Offline')

    ax.set_xlabel('Raio de Percepção')
    ax.set_ylabel('Movimentos Totais')
    ax.set_title('Movimentos Totais por Raio de Percepção')
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'movimentos_totais.png'), dpi=150)
    plt.close()


def plot_revealed_vs_revisited(results, output_dir):
    """Células reveladas vs revisitadas."""
    radii = sorted(results.keys())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for idx, algo in enumerate(['replanning_astar', 'online_dfs']):
        revealed = [results[r][algo]['cells_revealed'] for r in radii]
        revisited = [results[r][algo]['cells_revisited'] for r in radii]

        ax = axes[idx]
        x = range(len(radii))
        width = 0.35
        ax.bar([i - width/2 for i in x], revealed, width, label='Reveladas', color='#4CAF50')
        ax.bar([i + width/2 for i in x], revisited, width, label='Revisitadas', color='#F44336')

        title = 'Replanning A*' if algo == 'replanning_astar' else 'Online DFS'
        ax.set_title(f'{title}: Células Reveladas vs Revisitadas')
        ax.set_xlabel('Raio de Percepção')
        ax.set_ylabel('Número de Células')
        ax.set_xticks(x)
        ax.set_xticklabels(radii)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reveladas_vs_revisitadas.png'), dpi=150)
    plt.close()


def plot_replannings(results, output_dir):
    """Número de replanejamentos por raio."""
    radii = sorted(results.keys())
    replan_astar = [results[r]['replanning_astar']['replannings'] for r in radii]
    replan_dfs = [results[r]['online_dfs']['replannings'] for r in radii]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(radii, replan_astar, 'o-', color='#2196F3', linewidth=2, markersize=8, label='Replanning A*')
    ax.plot(radii, replan_dfs, 's-', color='#FF9800', linewidth=2, markersize=8, label='Online DFS')

    ax.set_xlabel('Raio de Percepção')
    ax.set_ylabel('Número de Replanejamentos')
    ax.set_title('Replanejamentos por Raio de Percepção')
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'replanejamentos.png'), dpi=150)
    plt.close()


def plot_execution_time(results, output_dir):
    """Tempo de execução por algoritmo e raio."""
    radii = sorted(results.keys())
    time_astar = [results[r]['replanning_astar']['time'] * 1000 for r in radii]  # ms
    time_dfs = [results[r]['online_dfs']['time'] * 1000 for r in radii]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(radii))
    width = 0.35

    ax.bar([i - width/2 for i in x], time_astar, width, label='Replanning A*', color='#2196F3')
    ax.bar([i + width/2 for i in x], time_dfs, width, label='Online DFS', color='#FF9800')

    ax.set_xlabel('Raio de Percepção')
    ax.set_ylabel('Tempo de Execução (ms)')
    ax.set_title('Tempo de Execução por Raio de Percepção')
    ax.set_xticks(x)
    ax.set_xticklabels(radii)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'tempo_execucao.png'), dpi=150)
    plt.close()


def plot_comparison_bars(results, output_dir):
    """Comparação geral entre algoritmos (raio=1)."""
    r = min(results.keys())
    res = results[r]

    metrics_names = ['Custo Real', 'Revisitadas', 'Replanejamentos']
    astar_vals = [
        res['replanning_astar']['real_cost'],
        res['replanning_astar']['cells_revisited'],
        res['replanning_astar']['replannings']
    ]
    dfs_vals = [
        res['online_dfs']['real_cost'],
        res['online_dfs']['cells_revisited'],
        res['online_dfs']['replannings']
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(metrics_names))
    width = 0.35

    ax.bar([i - width/2 for i in x], astar_vals, width, label='Replanning A*', color='#2196F3')
    ax.bar([i + width/2 for i in x], dfs_vals, width, label='Online DFS', color='#FF9800')

    ax.set_xlabel('Métrica')
    ax.set_ylabel('Valor')
    ax.set_title(f'Comparação Geral (Raio de Percepção = {r})')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_names)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparacao_geral.png'), dpi=150)
    plt.close()


def plot_discovery_progression(results, output_dir):
    """Progressão da descoberta do mapa ao longo do tempo."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for algo, label, color in [('replanning_astar', 'Replanning A*', '#2196F3'),
                                ('online_dfs', 'Online DFS', '#FF9800')]:
        states = results[algo]['map_states']
        discovery = []
        for state in states:
            known = sum(1 for row in state['map'] for cell in row if cell != '?')
            discovery.append(known)

        ax.plot(range(len(discovery)), discovery, color=color, linewidth=1.5, label=label)

    ax.set_xlabel('Passo')
    ax.set_ylabel('Células Conhecidas')
    ax.set_title('Progressão da Descoberta do Mapa')
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'progressao_descoberta.png'), dpi=150)
    plt.close()
