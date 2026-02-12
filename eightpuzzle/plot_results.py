import csv
import matplotlib.pyplot as plt

def plot_results(csv_file='test_results.csv'):
    """Read CSV and create comparison plots for nodes and time"""
    
    # Read data from CSV
    data_nodes = {'UCS': {}, 'A* Misplaced': {}, 'A* Manhattan': {}}
    data_time = {'UCS': {}, 'A* Misplaced': {}, 'A* Manhattan': {}}
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            algo = row['algorithm']
            depth = row['depth']
            nodes = row['nodes']
            time_s = row['time_s']
            
            # Skip timeouts and invalid data
            if depth in ['TIMEOUT', 'N/A'] or nodes in ['N/A', 'TIMEOUT']:
                continue
            
            depth = int(depth)
            nodes = int(nodes)
            time_s = float(time_s)
            
            # Store data
            if algo in data_nodes:
                data_nodes[algo][depth] = nodes
                data_time[algo][depth] = time_s
    
    # Colors for consistency
    colors = {'UCS': '#1f77b4', 'A* Misplaced': '#ff7f0e', 'A* Manhattan': '#2ca02c'}
    
    # Get all depths for x-axis
    all_depths = set()
    for points in data_nodes.values():
        all_depths.update(points.keys())
    all_depths = sorted(all_depths)
    
    # PLOT 1: Nodes Expanded
    plt.figure(figsize=(12, 7))
    
    for algo, points in data_nodes.items():
        if points:
            depths = sorted(points.keys())
            nodes = [points[d] for d in depths]
            plt.plot(depths, nodes, 
                    marker='o',
                    markersize=4,
                    label=algo, 
                    linewidth=2,
                    color=colors.get(algo))
    
    plt.xlabel('Depth of Optimal Solution', fontsize=13)
    plt.ylabel('Number of Nodes Expanded', fontsize=13)
    plt.title('Algorithm Comparison: Nodes Expanded', fontsize=15, fontweight='bold')
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(all_depths)
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison_nodes.png', dpi=300, bbox_inches='tight')
    print("Plot 1 saved as: algorithm_comparison_nodes.png")
    
    # PLOT 2: Time
    plt.figure(figsize=(12, 7))
    
    for algo, points in data_time.items():
        if points:
            depths = sorted(points.keys())
            times = [points[d] for d in depths]
            plt.plot(depths, times, 
                    marker='o',
                    markersize=4,
                    label=algo, 
                    linewidth=2,
                    color=colors.get(algo))
    
    plt.xlabel('Depth of Optimal Solution', fontsize=13)
    plt.ylabel('Time (seconds)', fontsize=13)
    plt.title('Algorithm Comparison: Execution Time', fontsize=15, fontweight='bold')
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(all_depths)


    
    plt.tight_layout()
    plt.savefig('algorithm_comparison_time.png', dpi=300, bbox_inches='tight')
    print("Plot 2 saved as: algorithm_comparison_time.png")
    
    # Show both plots
    plt.show()


if __name__ == "__main__":
    plot_results()